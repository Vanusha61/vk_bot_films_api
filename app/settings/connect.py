from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.settings.config import DATA_URL


created_engine = create_async_engine(
    url=DATA_URL,
)

created_session = async_sessionmaker(
    bind=created_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# async def sessions():
#     try:
#         async with created_session() as session:
#             yield session
#     finally:
#         await session.close()