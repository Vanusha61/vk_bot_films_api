import logging

from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import History



async def add_history(db: AsyncSession, user_id: int, user_name: str, command: str, query: str, result_preview: str, next_page: str = None, prev_page: str = None) -> bool:
    try:
        history = History(
            user_vk_id = user_id,
            user_name = user_name,
            command = command,
            query = query,
            result_preview = result_preview,
            next_page_url = next_page,
            prev_page_url = prev_page,
        )
        db.add(history)
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        logging.error(f"DB error add_history: {e}")
        return False

async def result_history(user_id: int, db: AsyncSession) -> List[History] | None:
    try:
        history = await db.execute(select(History).where(History.user_vk_id == user_id))
        return history.scalars().all()
    except Exception as e:
        logging.error(f"DB error result_history: {e}")
        return None

async def viewing_films(db: AsyncSession, user_id: int, film_name: str) -> History | None:
    try:
        result = await db.execute(
            select(History).where(History.user_vk_id == user_id, History.query == film_name, History.is_watched == False)
        )
        res = result.scalar_one_or_none()
        if not res:
            return None
        res.is_watched = True
        await db.commit()
        await db.refresh(res)
        return res
    except Exception as e:
        logging.error(f"DB error viewing_films: {e}")
        return None

async def new_evaluation(db: AsyncSession, user_id: int, film_name: str, numbers: int) -> History | bool | None:
    try:
        history = await db.execute(
            select(History).where(History.user_vk_id == user_id, History.query == film_name)
        )
        res = history.scalar_one()
        if not res:
            return False
        res.evaluation = numbers
        await db.commit()
        await db.refresh(res)
        return res
    except Exception as e:
        logging.error(f"DB error new_evaluation: {e}")
        await db.rollback()
        return None

async def info_film_name(db: AsyncSession, user_id: int, film_name: str) -> History | None:
    try:
        result = await db.execute(
            select(History).where(History.user_vk_id == user_id, History.query == film_name)
        )
        res = result.scalar_one_or_none()
        if not res:
            return None
        return res
    except Exception as e:
        logging.error(f"DB error info_film_name: {e}")
        return None

async def result_history_date(user_id: int, db: AsyncSession, start_date: datetime , end_date: datetime) -> List[History] | None:
    try:
        history = await db.execute(
            select(History).where(History.user_vk_id == user_id, History.created_at.between(start_date, end_date)).order_by(History.created_at.desc())
        )
        return history.scalars().all()
    except Exception as e:
        logging.error(f"DB error result_history: {e}")
        return None