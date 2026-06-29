import logging

from fastvk import Router
from fastvk.filters import Text
from fastvk.types import Message
from fastvk.fsm import FSMContext

from app.api.kinopoisk import film_filter_budget_low
from app.fsm.fsm_budget import BudgetStatesMin
from app.keyboards.reply import keyboard_budget_min_film,keyboard_menu


router_budget = Router()

@router_budget.message(Text("Низкий бюджет"))
async def start_budget(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(BudgetStatesMin.budget_mins)
    await message.answer("Введите бюджен, поиск будет проходить от 0 до вашего буджета")

@router_budget.message(BudgetStatesMin.budget_mins)
async def search_budget_min(message: Message, state: FSMContext):
    try:
        if float(message.text) < 0:
            await message.answer("Видите число больше 0")
            return
        await state.update_data(budget_min=float(message.text))
        await show_results(message, state)
    except Exception as e:
        logging.error(f"Error Api budget_min: {e}")
        await message.answer("Попробуйте позже")

async def show_results(message: Message, state: FSMContext, next_page: str = None, prev_page: str = None):
    try:
        data = await state.get_data()
        min_b = data["budget_min"]
        result = await film_filter_budget_low(float(min_b), next_page=next_page, prev=prev_page)
        if not result:
            await message.answer("Нет результата")
            return
        from pprint import pprint
        next_page = result.get(1, None).get("Next", None)
        prev_page = result.get(1, None).get("Prev", None)
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

        await message.answer("\n".join(parts), keyboard=keyboard_budget_min_film())
        await state.set_state(BudgetStatesMin.page)
        await state.update_data(next_page=next_page, prev_page=prev_page)
    except Exception as e:
        logging.error(f"Error Api budget_min: {e}")

@router_budget.message(Text("Назад"))
async def budget_back(message: Message, state: FSMContext):
    data = await state.get_data()
    next_page = data["next_page"]
    prev_page = data["prev_page"]
    if prev_page is None:
        await message.answer("Это первая страница")
        return
    await show_results(message, state, next_page=next_page, prev_page=prev_page)

@router_budget.message(Text("Вперед"))
async def budget_next(message: Message, state: FSMContext):
    data = await state.get_data()
    next_page = data["next_page"]
    prev_page = data["prev_page"]
    if next_page is None:
        await message.answer("Это последния страница")
        return
    await show_results(message, state, next_page=next_page, prev_page=prev_page)

@router_budget.message(Text("Выход"))
async def budget_exit(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Поиск завершён.", keyboard=keyboard_menu())
