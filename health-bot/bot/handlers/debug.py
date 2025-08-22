from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.storage.db import SessionLocal
from bot.storage.crud import get_user_by_tg

router = Router()

@router.message(Command("me"))
async def me(msg: Message):
    """Показать мой профиль из БД"""
    db = SessionLocal()
    try:
        user = get_user_by_tg(db, msg.from_user.id)
        if not user:
            await msg.answer("Профиль не найден. Пройди /profile сначала")
            return
        
        text = ("<b>Твой профиль</b>\n"
            f"id: {user.id}, tg_id: {user.tg_id}\n"
            f"Имя: {user.name}\nПол: {user.sex}, Возраст: {user.age}\n"
            f"Рост: {user.height} см, Вес: {user.weight} кг\n"
            f"Цель: {user.goal}, Активность: {user.activity}\n"
            f"Нормы: {user.kcal} ккал / Б:{user.protein_g} Ж:{user.fat_g} У:{user.carbs_g}\n"
            f"Премиум: {bool(user.is_premium)}\n"
        )
        await msg.answer(text)
    finally:
        db.close()

        
