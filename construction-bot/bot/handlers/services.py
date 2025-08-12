from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.keyboards import main_menu

router = Router()

# Кнопки
BTN_BACK = KeyboardButton(text="🔙 Назад")
BTN_HOME = KeyboardButton(text="⬅️ Возврат в главное меню")

# Подменю "Услуги"
services_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛠 Ремонт квартир под ключ")],
        [KeyboardButton(text="🏡 Строительство домов")],
        [KeyboardButton(text="📐 Проектирование домов")],
        [BTN_HOME, BTN_BACK],
    ],
    resize_keyboard=True
)

@router.message(StateFilter(None), F.text == "🏗 Услуги")
async def services_menu(message: Message):
    await message.answer(
        "Выберите категорию услуги:",
        reply_markup=services_kb
    )

@router.message(StateFilter(None), F.text == "🛠 Ремонт квартир под ключ")
async def service_repair(message: Message):
    await message.answer(
        "🛠 Ремонт любой сложности: от косметического до капитального.\n"
        "Гарантия, качество и соблюдение сроков.",
        reply_markup=services_kb
    )

@router.message(StateFilter(None), F.text == "🏡 Строительство домов")
async def service_build(message: Message):
    await message.answer(
        "🏡 Строим дома, коттеджи и таунхаусы под ключ.\n"
        "Современные технологии и качественные материалы.",
        reply_markup=services_kb
    )

@router.message(StateFilter(None), F.text == "📐 Проектирование домов")
async def service_design(message: Message):
    await message.answer(
        "📐 Проектирование жилых и коммерческих объектов с учётом ваших требований.",
        reply_markup=services_kb
    )

@router.message(StateFilter(None), F.text == "🔙 Назад")
async def back_to_services(message: Message):
    await services_menu(message)

@router.message(StateFilter(None), F.text == "⬅️ Возврат в главное меню")
async def back_home(message: Message):
    await message.answer("🏠 Главное меню", reply_markup=main_menu())
