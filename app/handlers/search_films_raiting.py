import logging

from fastvk import Router
from fastvk.types import Message
from fastvk.filters import Text
from fastvk.fsm import FSMContext

from app.api.kinopoisk import film_filter_cursor
from app.fsm.film_filter_fsm import SearchFilmRating
from app.keyboards.reply import keyboard_rating_film, keyboard_menu

router_rating = Router()

@router_rating.message(Text("По рейтингу"))
async def start_rating(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(SearchFilmRating.rating)
    await message.answer("Введите рейтинг фильмов от 1 до 10")

@router_rating.message(SearchFilmRating.rating)
async def rating(message: Message, state: FSMContext):
    try:
        await state.update_data(rating=message.text)
        await show_results(message, state)
    except Exception as e:
        logging.error(f"Film_name API error: {e}", exc_info=True)
        await message.answer("Попробуйте позже")

async def show_results(message: Message, state: FSMContext, next_page_c = None, prev_page_c = None):
    try:
        data = await state.get_data()
        r = data["rating"]
        result = await film_filter_cursor(r, next_page=next_page_c, prev=prev_page_c)
        if not result:
            await message.answer("Ничего не найдено или ошибка API.")
            await state.clear()
            return
        next_page = result.get(1).get("Next", None)
        prev_page = result.get(1).get("Prev", None)
        await state.update_data(next_page=next_page, prev_page=prev_page)
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

        await message.answer("\n".join(parts), keyboard=keyboard_rating_film())
        await state.set_state(SearchFilmRating.page)
    except Exception as e:
        logging.error(f"Film_rating API error: {e}", exc_info=True)

@router_rating.message(Text("🚪 Выход"))
async def exit_rating(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Поиск завершён.", keyboard=keyboard_menu())

@router_rating.message(Text("🔜"))
async def next_rating(message: Message, state: FSMContext):
    data = await state.get_data()
    next_p = data["next_page"]
    prev_p = data["prev_page"]
    if next_p is not None:
        await show_results(message, state, next_page_c = next_p, prev_page_c = prev_p)
    else:
        await message.answer("Это последния сраница")
        return

@router_rating.message(Text("🔙"))
async def prev_rating(message: Message, state: FSMContext):
    data = await state.get_data()
    next_p = data["next_page"]
    prev_p = data["prev_page"]
    if prev_p is not None:
        await show_results(message, state, prev_page_c = prev_p, next_page_c = next_p)
    else:
        await message.answer("Это первая станица")
        return


