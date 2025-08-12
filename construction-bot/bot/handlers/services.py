from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.keyboards import services_menu, main_menu

router = Router()

back_to_services_btn = KeyboardButton(text="⬅️ Назад")
back_to_main_btn = KeyboardButton(text="🏠 Возврат в главное меню")

def back_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[back_to_services_btn], [back_to_main_btn]],
        resize_keyboard=True
    )

@router.message(F.text == "📐 Проектирование домов")
async def handle_design(message: Message):
    await message.answer(
        "📐 Проектирование жилых и коммерческих объектов.\n"
        "Учитываем пожелания и делаем оптимальный проект.",
        reply_markup=back_kb()
    )

@router.message(F.text == "🛠 Ремонт квартир под ключ")
async def handle_renovation(message: Message):
    await message.answer(
        "🛠 Ремонт любой сложности: от косметического до капитального. "
        "Гарантия, качество, сроки.",
        reply_markup=back_kb()
    )

@router.message(F.text == "🏡 Строительство домов")
async def handle_construction(message: Message):
    await message.answer(
        "🏡 Строим дома и коттеджи под ключ. Современные технологии и материалы.",
        reply_markup=back_kb()
    )


@router.message(F.text == "⬅️ Назад")
async def back_to_services(message: Message):
    await message.answer("Выберите услугу:", reply_markup=services_menu())

@router.message(F.text == "🏠 Возврат в главное меню")
async def back_to_main(message: Message):
    await message.answer("Главное меню:", reply_markup=main_menu())
