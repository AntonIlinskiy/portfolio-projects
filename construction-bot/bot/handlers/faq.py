from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.keyboards import main_menu

router = Router()

back = KeyboardButton(text="🔙 Назад")
_back_main = KeyboardButton(text="⬅️ Возврат в главное меню")

FAQ_ITEMS = {
    "Сроки ремонта": "Срок зависит от площади и вида работ. Квартира 40–60 м² — обычно 4–8 недель.",
    "Гарантия": "12 месяцев на работы. Материалы — по гарантии производителя.",
    "Смета и договор": "Делаем бесплатную смету, фиксируем в договоре этапы и сроки.",
    "Черновые материалы": "Можем закупать сами или работать с вашими поставщиками.",
}

def faq_menu() -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text= title)] for title in FAQ_ITEMS.keys()]
    rows += [[back], [_back_main]]
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

@router.message(F.text == "❓ FAQ")
async def faq_entry(message: Message):
    await message.answer("Выберите вопрос:", reply_markup=faq_menu())

@router.message(F.text.in_(list(FAQ_ITEMS.keys())))
async def faq_answer(message: Message):
    await message.answer(f"❓ {message.text}\n\n{FAQ_ITEMS[message.text]}", reply_markup=faq_menu())

@router.message(F.text == "🔙 Назад")
async def faq_back(message: Message):
    await message.answer("🏠 Главное меню", reply_markup=main_menu())

@router.message(F.text == "⬅️ Возврат в главное меню")
async def faq_back_main(message: Message):
    await message.answer("🏠 Главное меню", reply_markup=main_menu())    