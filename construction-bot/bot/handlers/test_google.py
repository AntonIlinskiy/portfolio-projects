from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime

from services.gsheets import append_lead_row

router = Router()

@router.message(Command("test_google"))
async def test_google_handler(message: Message):
    try:
        append_lead_row(
            when=datetime.now(),
            name="Тест",
            phone="+7 999 000-00-00",
            username=message.from_user.username,
            source="Telegram",
            service="Test service",
            comment="Тестовая запись",
        )
        await message.answer("✅ Google Sheets: запись добавлена")
    except Exception as e:
        await message.answer(f"❌ Google Sheets: ошибка\n{e}")
