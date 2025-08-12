from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

_back_main = KeyboardButton(text="⬅️ Возврат в главное меню")

@router.message(F.text == "ℹ️ О компании")
async def about_company(message: Message):
    text = (
        "🏗 Наша компания занимается строительством и ремонтом более 10 лет.\n"
        "Мы предлагаем:\n"
        "— Индивидуальный подход\n"
        "— Гарантию качества\n"
        "— Соблюдение сроков\n"
    )
    await message.answer(
        text,
        reply_markup=ReplyKeyboardMarkup(keyboard=[[ _back_main ]], resize_keyboard=True)
    )

@router.message(F.text == "📞 Контакты")
async def contacts(message: Message):
    text = (
        "📞 Телефон: +7 (999) 123-45-67\n"
        "✉️ Email: info@example.com"
    )
    await message.answer(
        text,
        reply_markup=ReplyKeyboardMarkup(keyboard=[[ _back_main ]], resize_keyboard=True)
    )
