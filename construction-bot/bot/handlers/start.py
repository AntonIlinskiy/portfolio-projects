from aiogram import Router, types
from aiogram.types import Message
from bot.keyboards import main_menu

Router = Router()

@router.message(commands=["start"])
async def start_handler(message: Message):
    await message.answer(
        text="👋 Добро пожаловать!\n\nЯ — бот, который поможет вам с ремонтом, строительством и проектированием.",
        reply_markup=main_menu()
    )
