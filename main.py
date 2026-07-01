import asyncio

from fastvk import FastVK

from app.settings.config import vk_bot_api
from app.handlers.start import router
from app.handlers.category import router_category
from app.handlers.h_film_name_search import router_film_name
from app.handlers.search_films_raiting import router_rating
from app.handlers.search_budget import router_budget
from app.handlers.search_budget_max import router_budget_max
from app.handlers.history_info import router_history
from app.api.kinopoisk import client

bot = FastVK(token=vk_bot_api)

bot.include_router(router)
bot.include_router(router_category)
bot.include_router(router_film_name)
bot.include_router(router_rating)
bot.include_router(router_budget)
bot.include_router(router_budget_max)
bot.include_router(router_history)

if __name__ == "__main__":
    try:
        bot.run_polling()
    except Exception as e:
        print(e)
    finally:
        asyncio.run(client.aclose())