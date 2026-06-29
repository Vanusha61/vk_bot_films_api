import logging

from fastvk import Router

from fastvk.filters import Text
from fastvk.types import Message

from app.api.kinopoisk import search_category_films

router_category = Router()

@router_category.message(Text("Список жанров"))
async def category_message(message: Message):
    try:
        res = await search_category_films()
        if res is None:
            await message.answer("Не удалось получить список жанров. Попробуйте позже.")
            return
        reply = f"Жанры: {", ".join(res)}\n"
        await message.answer(reply)
    except Exception as e:
        logging.error(f"Kinopoisk API error: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")