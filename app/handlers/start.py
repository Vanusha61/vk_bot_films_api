from fastvk import Router

from fastvk.filters import Command, Text
from fastvk.types import Message

from app.keyboards.reply import keyboard_menu


router = Router()
@router.message(Command("start", "начать", "Начать"))
async def start(message: Message):
    await message.answer("Выберите кнопку: ", keyboard=keyboard_menu())

@router.message(Text("start", "начать", "Начать"))
async def start_t(message: Message):
    await message.answer("Выберите кнопку: ", keyboard=keyboard_menu())
