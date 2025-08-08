from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

# Кнопки для возврата
back_to_services = KeyboardButton(text="🔙 Назад")
back_to_main = KeyboardButton(text="⬅️ Возврат в главное меню")

# Обработчик кнопки "Проектирование домов"
@router.message(F.text == "📐 Проектирование домов")
async def handle_design(message: Message):
    await message.answer(
        "📐 Мы предлагаем услуги по проектированию жилых и коммерческих объектов.\n"
        "Наши архитекторы учтут все ваши пожелания и создадут оптимальный проект.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[back_to_services], [back_to_main]],
            resize_keyboard=True
        )
    )

# Обработчик кнопки "Ремонт квартир под ключ"
@router.message(F.text == "🛠 Ремонт квартир под ключ")
async def handle_renovation(message: Message):
    await message.answer(
        "🛠 Мы выполняем ремонт любой сложности: от косметического до капитального.\n"
        "Гарантия, качество, соблюдение сроков — всё включено!",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[back_to_services], [back_to_main]],
            resize_keyboard=True
        )
    )

# Обработчик кнопки "Строительство домов"
@router.message(F.text == "🏡 Строительство домов")
async def handle_construction(message: Message):
    await message.answer(
        "🏡 Строим загородные дома, коттеджи и таунхаусы под ключ.\n"
        "Используем качественные материалы и современные технологии.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[back_to_services], [back_to_main]],
            resize_keyboard=True
        )
    )
