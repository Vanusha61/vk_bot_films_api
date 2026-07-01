import httpx
import logging

from app.settings.config import api_list_category_films, x_api_key, film_name, film_filters_cursor

client = httpx.AsyncClient(timeout=30.0)

async def search_category_films() -> set[str] | None:
    try:
        headers = {
            "X-API-KEY": x_api_key
        }
        response_category_films = await client.get(url=api_list_category_films, headers=headers)
        response_category_films.raise_for_status()
        res = response_category_films.json()
        result = set(
            i.get("name", "")
            for i in res
        )
        return result
    except Exception as e:
        logging.error(e)
        return None

async def search_films(film_n: str, page: int = 1, limit: int = 5) -> dict[str, str] | None:
    try:
        headers = {
            "X-API-KEY": x_api_key
        }
        params = {
            "query": film_n,
            "page": page,
            "limit": limit
        }
        response_films = await client.get(url=film_name, headers=headers, params=params)
        response_films.raise_for_status()
        res = response_films.json()
        films_dict = {}
        pages_dict = 0
        for f in res.get('docs', []):
            d = {}
            d["Название"] = f.get('alternativeName', "")
            d["Страна"] = f.get('countries', [{}])[0].get('name', "Неизвестно") if f.get("countries") else "Неизвестно"
            d["Описание"] = f.get('description', "Описание отсутствует")
            d["Жанр"] = ", ".join([i.get("name", "") for i in f.get('genres', []) if i.get("name")])
            d["Рейтинг"] = f.get('rating', {}).get('imdb', "Нет рейтинга") if f.get("rating") else "Нет рейтинга"
            d["Выпуск"] = f.get('year', "Неизвестно")
            d["Постер"] = f.get("poster", {}).get("url", "Фото отсутствует")
            pages_dict += 1
            films_dict[pages_dict] = d
        return films_dict
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return None


async def film_filter_cursor(rating: int, limit: int = 5, next_page: str = None, prev: str = None) -> dict[int, str] | None:
    try:
        filters = {
            "rating.kp": rating,
            "limit": limit,
            "next": next_page,
            "prev": prev
        }
        headers = {
            "X-API-KEY": x_api_key
        }
        response = await client.get(url=film_filters_cursor, params=filters, headers=headers)
        response.raise_for_status()
        res = response.json()
        films_dict = {}
        pages_dict = 0
        for film in res['docs']:
            d = {}
            d["Название"] = film.get('alternativeName', "")
            d["Страна"] = film.get('countries', [{}])[0].get('name', "Неизвестно") if film.get("countries") else "Неизвестно"
            d["Описание"] = film.get('description', "Описание отсутствует")
            d["Жанр"] = ", ".join([i.get("name", "") for i in film.get('genres', []) if i.get("name")])
            d["Рейтинг"] = film.get('rating', {}).get('kp', 'Рейтинг отсутствует')
            d["Выпуск"] = film.get('year', "Неизвестно")
            d["Постер"] = film.get("poster", {}).get("url", "Фото отсутствует")
            d["Next"] = res.get("next")
            d["Prev"] = res.get("prev")
            pages_dict += 1
            films_dict[pages_dict] = d
        return films_dict
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

async def film_filter_budget_low(min_budget: float, next_page: str = None, prev: str = None) -> dict[int, str] | None:
    try:
        headers = {
            "X-API-KEY": x_api_key
        }
        filters = {
            "budget.value": f"{0}-{min_budget}",
            "limit": 5,
            "next": next_page,
            "prev": prev
        }
        response = await client.get(url=film_filters_cursor, headers=headers, params=filters)
        response.raise_for_status()
        res = response.json()
        films_dict = {}
        pages_dict = 0
        for film in res['docs']:
            d = {}
            d["Название"] = film.get('alternativeName', "")
            d["Страна"] = film.get('countries', [{}])[0].get('name', "Неизвестно") if film.get("countries") else "Неизвестно"
            d["Описание"] = film.get('description', "Описание отсутствует")
            d["Жанр"] = ", ".join([i.get("name", "") for i in film.get('genres', []) if i.get("name")])
            d["Рейтинг"] = film.get('rating', {}).get('kp', 'Рейтинг отсутствует')
            d["Выпуск"] = film.get('year', "Неизвестно")
            d["Постер"] = film.get("poster", {}).get("url", "Фото отсутствует")
            d["Next"] = res.get("next")
            d["Prev"] = res.get("prev")
            pages_dict += 1
            films_dict[pages_dict] = d
        return films_dict
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None


async def film_filter_budget_max(max_budget: float, next_page: str = None, prev: str = None) -> dict[int, str] | None:
    try:
        headers = {
            "X-API-KEY": x_api_key
        }
        filters = {
            "budget.value": f"{max_budget}-{10_000_000_000}",
            "limit": 5,
            "next": next_page,
            "prev": prev
        }
        response = await client.get(url=film_filters_cursor, headers=headers, params=filters)
        response.raise_for_status()
        res = response.json()
        films_dict = {}
        pages_dict = 0
        for film in res['docs']:
            d = {}
            d["Название"] = film.get('alternativeName', "")
            d["Страна"] = film.get('countries', [{}])[0].get('name', "Неизвестно") if film.get(
                "countries") else "Неизвестно"
            d["Описание"] = film.get('description', "Описание отсутствует")
            d["Жанр"] = ", ".join([i.get("name", "") for i in film.get('genres', []) if i.get("name")])
            d["Рейтинг"] = film.get('rating', {}).get('kp', 'Рейтинг отсутствует')
            d["Выпуск"] = film.get('year', "Неизвестно")
            d["Постер"] = film.get("poster", {}).get("url", "Фото отсутствует")
            d["Next"] = res.get("next")
            d["Prev"] = res.get("prev")
            pages_dict += 1
            films_dict[pages_dict] = d
        return films_dict
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

