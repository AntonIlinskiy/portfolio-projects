from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards import main_menu

router = Router()

@router.message(F.text == "⬅️ Назад в меню")
@router.message(F.text == "/start")
async def start_cmd(message: Message):
    await message.answer(
        "👋 Привет! Я бот записи на ТО автомобиля.\nВыберите действие:",
        reply_markup=main_menu()
    )

@router.message(F.text == "ℹ️ Услуги")
async def services_info(message: Message):
    await message.answer(
        "🛠 Доступные услуги:\n• ТО-1\n• ТО-2\n• Диагностика\n• Замена масла\n\nНажмите «🗓 Записаться на ТО», чтобы выбрать дату и время.",
        reply_markup=main_menu()
    )

@router.message(F.text == "📞 Контакты")
async def contacts(message: Message):
    await message.answer(
        "☎️ Телефон: +7 900 000-00-00\n📧 Email: service@example.com",
        reply_markup=main_menu()
    )