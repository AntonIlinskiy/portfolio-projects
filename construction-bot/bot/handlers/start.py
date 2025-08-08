from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.keyboards import main_menu, services_menu  # импортируем готовые меню
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        text="👋 Добро пожаловать!\n\nЯ — бот, который поможет вам с ремонтом, строительством и проектированием.",
        reply_markup=main_menu()
    )


@router.message(lambda message: message.text == "🏗 Услуги")
async def services_handler(message: Message):
    await message.answer(
        text="Выберите интересующую услугу:",
        reply_markup=services_menu()
    )

@router.message(lambda message: message.text == "🔙 Назад")
async def back_to_main(message: Message):
    await message.answer("🔙 Возврат в главное меню", reply_markup=main_menu())

# 🔙 Назад → возвращаем пользователя в меню «Услуги»
@router.message(F.text == "🔙 Назад")
async def back_to_services(message: Message):
    await message.answer("📋 Выберите услугу:", reply_markup=services_menu())

# ⬅️ Возврат в главное меню
@router.message(F.text == "⬅️ Возврат в главное меню")
async def back_to_main(message: Message):
    await message.answer("🏠 Главное меню", reply_markup=main_menu())