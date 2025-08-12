from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from collections import defaultdict
from bot.keyboards import main_menu
import os

router = Router()

# 🖼 Пути к фото и тексты отзывов
BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "reviews")
REVIEWS = [
    {
        "photo": os.path.join(BASE, "review1.jpg"),
        "text": "«Сделали ремонт квартиры в срок и очень аккуратно. Команда — профессионалы»\n— Анна, Москва",
    },
    {
        "photo": os.path.join(BASE, "review2.jpg"),
        "text": "«Строили дом по проекту. Качество материалов и работы на высоте, всем советую!»\n— Сергей, МО",
    },
    {
        "photo": os.path.join(BASE, "review3.jpg"),
        "text": "«Проектирование + реализация. Помогли оптимизировать бюджет без потери качества.»\n— Ирина, Москва",
    },
]

# Позиции просмотра по пользователю (простой цикл без FSM)
_positions = defaultdict(int)

def _reviews_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➡️ Следующий отзыв")],
            [KeyboardButton(text="⬅️ Возврат в главное меню")],
        ],
        resize_keyboard=True
    )

async def _send_review(message: Message, idx: int):
    item = REVIEWS[idx]
    photo_path = item["photo"]
    if not os.path.exists(photo_path):
        await message.answer(f"⚠️ Фото не найдено: {os.path.basename(photo_path)}")
        return
    await message.answer_photo(
        photo=FSInputFile(photo_path),
        caption=item["text"],
        reply_markup=_reviews_kb(),
    )

@router.message(F.text == "💬 Отзывы клиентов")
async def reviews_open(message: Message):
    _positions[message.from_user.id] = 0
    await _send_review(message, 0)

@router.message(F.text == "➡️ Следующий отзыв")
async def reviews_next(message: Message):
    uid = message.from_user.id
    _positions[uid] = (_positions[uid] + 1) % len(REVIEWS)
    await _send_review(message, _positions[uid])

@router.message(F.text == "⬅️ Возврат в главное меню")
async def reviews_back_to_main(message: Message):
    await message.answer("🏠 Главное меню", reply_markup=main_menu())