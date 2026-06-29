import logging

from fastvk import Router
from fastvk.filters import Text
from fastvk.types import Message
from fastvk.fsm import FSMContext

from app.api.kinopoisk import search_films
from app.fsm.search_states import SearchFilmName
from app.keyboards.reply import keyboard_pages_film_name, keyboard_menu

router_film_name = Router()

@router_film_name.message(Text("Поиск по названию"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(SearchFilmName.name)
    await message.answer("Напишите название фильма:")

@router_film_name.message(SearchFilmName.name)
async def film_names(message: Message, state: FSMContext) -> None:
    try:
        await state.update_data(name=message.text.strip(), page=1)
        await show_results(message, state)
    except Exception as e:
        logging.error(f"Film_name API error: {e}", exc_info=True)
        await message.answer("Попробуйте позже")


async def show_results(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    name = data.get("name")
    page = data.get("page")
    result = await search_films(film_n=name, page=page)
    if not result:
        await message.answer("Ничего не найдено.")
        await state.clear()
        return
    parts = ["🎬 **Результаты поиска:**\n"]
    for idx, film_info in result.items():
        parts.append(f"**{idx}: ")
        parts.append(f"Название: {film_info['Название']}")
        parts.append(f"📖 Описание: {film_info["Описание"]}")
        parts.append(f"📅 Год: {film_info['Выпуск']}")
        parts.append(f"🌍 Страна: {film_info['Страна']}")
        parts.append(f"🎭 Жанр: {film_info['Жанр']}")
        parts.append(f"⭐ Рейтинг: {film_info['Рейтинг']}")
        parts.append(f"🖼️ Постер: {film_info['Постер']}")


    sent_id = await message.answer("\n".join(parts), keyboard=keyboard_pages_film_name())

    await state.update_data(last_message_id=sent_id)
    await state.set_state(SearchFilmName.page)


@router_film_name.message(Text("➡️ Вперед"))
async def next_page_text(message: Message, state: FSMContext):
    data = await state.get_data()
    page = data.get("page", 1)
    if page >= 10:
        await message.answer("Это последняя страница!")
        return
    page += 1
    await state.update_data(page=page)
    await show_results(message, state)

@router_film_name.message(Text("⬅️ Назад"))
async def prev_page_text(message: Message, state: FSMContext):
    data = await state.get_data()
    page = data.get("page", 1)
    if page <= 1:
        await message.answer("Это первая страница.")
        return
    page -= 1
    await state.update_data(page=page)
    await show_results(message, state)

@router_film_name.message(Text("❌ Выход"))
async def exit_search_text(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Поиск завершён.", keyboard=keyboard_menu())

