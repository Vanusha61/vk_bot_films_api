from sqlalchemy import Column, Integer, VARCHAR, Text, DateTime, func, Boolean
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class History(Base):

    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_vk_id = Column(Integer, nullable=False)
    user_name = Column(VARCHAR(50), nullable=False)
    command = Column(VARCHAR(50), nullable=False)
    query = Column(VARCHAR(200), nullable=False)
    result_preview = Column(Text, nullable=False)
    next_page_url = Column(VARCHAR(200), nullable=True)
    prev_page_url = Column(VARCHAR(200), nullable=True)
    created_at = Column(DateTime, default=func.now())
    is_watched = Column(Boolean, default=False)
    evaluation = Column(Integer, default=False)