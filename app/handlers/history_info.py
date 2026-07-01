import logging

from fastvk import Router
from fastvk.filters import Text
from fastvk.fsm import FSMContext
from fastvk.types import Message

from datetime import datetime, timedelta

from app.db.crud import result_history, viewing_films, new_evaluation, result_history_date
from app.settings.connect import created_session
from app.keyboards.reply import keyboard_history_film, keyboard_menu, keyboard_history_date
from app.fsm.history import History, NewEvaluation, DateTimeFilm

router_history = Router()

@router_history.message(Text("История"))
async def history(message: Message, state: FSMContext) -> None:
    try:
        async with created_session() as s:
            result = await result_history(db=s, user_id=message.from_user.id)
            if not result:
                await message.answer("Ваше история пустая")
                return
            await state.update_data(history_list=result, page=0, max_pages=len(result))
            await show_history(message=message, state=state)
            await state.set_state(History.history_page)
    except Exception as err:
        logging.error("history handlers error", err)
        await message.answer("Попробуйте позже")

async def show_history(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    history_list = data.get("history_list")
    page = data.get("page")
    max_pages = data.get("max_pages")

    if page >= max_pages:
        await message.answer("Это последний фильм")
        page -= 1
        await state.update_data(page=page)
        return

    if page == -1:
        await message.answer("⏪ Это начало истории")
        page += 1
        await state.update_data(page=page)
        return

    result = history_list[page]
    res = ("Ваша история поиска: \n"
           f"стр: {page + 1} из {len(history_list)}\n")
    res += f"Команда: {result.command} \n"
    res += f"Запрос: {result.query} \n"
    res += f"Результат: {result.result_preview} \n"
    res += f"Дата поиска: {result.created_at} \n"
    res += f"Просмотрен: {result.is_watched} \n"
    res += f"Оценка: {result.evaluation} \n"
    await message.answer(res, keyboard=keyboard_history_film())
    await state.update_data(film_names=result.query, page=page)
    await state.set_state(History.viewing)

@router_history.message(Text("📖 Назад"))
async def history_page_prev(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    page = data.get("page")
    page -= 1
    await state.update_data(page=page)
    await show_history(message=message, state=state)


@router_history.message(Text("📖 Вперед"))
async def history_page_next(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    page = data.get("page")
    page += 1
    await state.update_data(page=page)
    await show_history(message=message, state=state)

@router_history.message(Text("🏁 Выход"))
async def history_exit(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Закрываю", keyboard=keyboard_menu())

@router_history.message(Text("✅ Просмотрено"))
async def history_viewing_films(message: Message, state: FSMContext) -> None:
    try:
        async with created_session() as s:
            data = await state.get_data()
            film_names = data.get("film_names")
            res = await viewing_films(db=s, user_id=message.from_user.id, film_name=film_names)
            if not res:
                await message.answer("Этот фильм уже смотрели!")
                await state.clear()
                return
            await state.set_state(History.evaluation)
            await message.answer("О вы посмотрели фильм, оставить оценку для себя от 1 до 10!")
    except Exception as err:
        logging.error(f"DB error result_history: {err}")

@router_history.message(History.evaluation)
async def film_evalution(message: Message, state: FSMContext) -> None:
    try:
        async with created_session() as s:
            data = await state.get_data()
            film_names = data.get("film_names")
            numbers = message.text.strip()
            result = await new_evaluation(db=s, user_id=message.from_user.id, film_name=film_names, numbers=int(numbers))
            res = ("Фильм обновлен: \n")
            res += f"Команда: {result.command} \n"
            res += f"Запрос: {result.query} \n"
            res += f"Результат: {result.result_preview} \n"
            res += f"Дата поиска: {result.created_at} \n"
            res += f"Просмотрен: {result.is_watched} \n"
            res += f"Оценка: {result.evaluation} \n"
            await message.answer(res, keyboard=keyboard_history_film())
            await state.clear()
    except Exception as err:
        logging.error(f"DB error result_history: {err}")
        await message.answer("Попробуйте похже!")
        await state.clear()
        return

@router_history.message(Text("Изменить оценку"))
async def start_evalution(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(NewEvaluation.film_name)
    await message.answer("Введите название фильма из вашего списка")

@router_history.message(NewEvaluation.film_name)
async def name_film_evalution(message: Message, state: FSMContext) -> None:
    film_name = message.text.strip()
    await state.update_data(film_name=film_name)
    await state.set_state(NewEvaluation.evaluation)
    await message.answer("Введите новую оценку просмотренего фильма")

@router_history.message(NewEvaluation.evaluation)
async def new_film_evalution(message: Message, state: FSMContext) -> None:
    try:
        async with created_session() as s:
            new_numbers = message.text.strip()
            data = await state.get_data()
            film_name = data.get("film_name")
            result = await new_evaluation(db=s, user_id=message.from_user.id, film_name=film_name, numbers=int(new_numbers))
            if not result:
                await message.answer("Такого фильма нет в списке", keyboard=keyboard_menu())
                await state.clear()
            res = ("Фильм обновлен: \n")
            res += f"Название фильма: {result.query} \n"
            res += f"Результат: {result.result_preview} \n"
            res += f"Дата поиска: {result.created_at} \n"
            res += f"Просмотрен: {result.is_watched} \n"
            res += f"Оценка: {result.evaluation} \n"
            await message.answer(res, keyboard=keyboard_menu())
            await state.clear()
    except Exception as err:
        logging.error(f"DB error result_history: {err}")
        await state.clear()
        return


@router_history.message(Text("История за дату"))
async def history_by_date_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(DateTimeFilm.start_date)
    await message.answer("📅 Введи дату в формате ДД.ММ.ГГГГ\n\n"
                         "Или напиши:\n"
                         "• 'сегодня' — за сегодня\n"
                         "• 'вчера' — за вчера\n"
                         "• 'неделя' — за последние 7 дней")

@router_history.message(DateTimeFilm.start_date)
async def history_by_date_new_start(message: Message, state: FSMContext):
    try:
        async with created_session() as s:
            start_date = message.text.strip().lower()
            if start_date == "сегодня":
                start_date=datetime.now().replace(hour=0,minute=0, second=0, microsecond=0)
                end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
            elif start_date == "вчера":
                start_date=(datetime.now() - timedelta(days=1)).replace(hour=0,minute=0, second=0, microsecond=0)
                end_date = (datetime.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)
            elif start_date == "неделя":
                start_date = datetime.now() - timedelta(days=7)
                end_date = datetime.now()
            else:
                start_date = datetime.strptime(message.text, "%d.%m.%Y")
                end_date = datetime.now()
            result = await result_history_date(user_id=message.from_user.id, start_date=start_date, end_date=end_date, db=s)
            if not result:
                await message.answer("📭 За этот период ничего не найдено")
                return
            await state.update_data(result_list=result, page=0, max_pages=len(result))
            await state.set_state(DateTimeFilm.page)
            await show_history_date(message=message, state=state)
    except Exception as err:
        logging.error(f"DB error history_by_date_start: {err}")
        await state.clear()
        return


async def show_history_date(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    result_list = data.get("result_list")
    page = data.get("page")
    max_pages = data.get("max_pages")

    if page >= max_pages:
        await message.answer("Это последний страница")
        page -= 1
        await state.update_data(page=page)
        return

    if page == -1:
        await message.answer("⏪ Это первая станица")
        page += 1
        await state.update_data(page=page)
        return

    result = result_list[page]
    res = ("Ваша история поиска: \n"
           f"стр: {page + 1} из {len(result_list)}\n")
    res += f"Команда: {result.command} \n"
    res += f"Запрос: {result.query} \n"
    res += f"Результат: {result.result_preview} \n"
    res += f"Дата поиска: {result.created_at} \n"
    res += f"Просмотрен: {result.is_watched} \n"
    res += f"Оценка: {result.evaluation} \n"
    await message.answer(res, keyboard=keyboard_history_date())
    await state.update_data(film_names=result.query, page=page)
    await state.set_state(History.viewing)

@router_history.message(Text("📚 Назад"))
async def history_by_date_back(message: Message, state: FSMContext):
    data = await state.get_data()
    page = data.get("page")
    page -= 1
    await state.update_data(page=page)
    await show_history_date(message=message, state=state)


@router_history.message(Text("📚 Вперед"))
async def history_by_date_next(message: Message, state: FSMContext):
    data = await state.get_data()
    page = data.get("page")
    page += 1
    await state.update_data(page=page)
    await show_history_date(message=message, state=state)

@router_history.message(Text("🔖 Выход"))
async def history_by_date_exit(message: Message, state: FSMContext):
    await message.answer("Выход...", keyboard=keyboard_menu())
    await state.clear()