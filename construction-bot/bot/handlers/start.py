from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.keyboards import main_menu, services_menu

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Добро пожаловать!\n\nЯ — бот, который поможет вам с ремонтом, строительством и проектированием.",
        reply_markup=main_menu()
    )

@router.message(lambda m: m.text == "📂 Портфолио")
async def open_portfolio(message: Message):
    from .portfolio import portfolio  # чтобы не было цикличного импорта
    await portfolio(message)

@router.message(lambda m: m.text == "📋 Услуги")
async def open_services(message: Message):
    await message.answer("Выберите интересующую услугу:", reply_markup=services_menu())

@router.message(F.text == "⬅️ Возврат в главное меню")
async def back_to_main(message: Message):
    await message.answer("🏠 Главное меню", reply_markup=main_menu())