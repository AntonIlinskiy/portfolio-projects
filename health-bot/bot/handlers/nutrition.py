# bot/handlers/nutrition.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.handlers.profile import USERS
from bot.services.nutrition import (
    bmr_mifflin, tdee, target_kcal, macros_for, format_macros
)
from bot.storage.db import SessionLocal
from bot.storage.crud import get_user_by_tg

router = Router()

def need_profile_text() -> str:
    return "Чтобы рассчитать нормы, заполни /profile (пол, возраст, рост, вес, цель, активность)."

@router.message(Command("norms"))
async def norms(msg: Message):
    db = SessionLocal()
    try:
        u = get_user_by_tg(db, msg.from_user.id)
        if not u or not all([u.sex, u.age, u.height, u.weight, u.goal, u.activity]):
            await msg.answer("Чтобы рассчитать нормы, заполни /profile.")
            return
        if u.kcal and u.protein_g:
            await msg.answer(
                "<b>Нормы на день</b>\n"
                f"Калории: <b>{u.kcal}</b> ккал\n"
                f"Белки: <b>{u.protein_g}</b> г\n"
                f"Жиры: <b>{u.fat_g}</b> г\n"
                f"Углеводы: <b>{u.carbs_g}</b> г\n"
            )
            return
    finally:
        db.close()

    await msg.answer("Нормы ещё не рассчитаны. Пройди /profile заново.")

@router.message(Command("menu"))
async def menu_day(msg: Message):
    u = USERS.get(msg.from_user.id)
    if not u or not all(k in u for k in ("sex","age","height","weight","goal","activity")):
        await msg.answer(need_profile_text())
        return

    bmr = bmr_mifflin(u["sex"], int(u["age"]), float(u["height"]), float(u["weight"]))
    daily = target_kcal(tdee(bmr, u["activity"]), u["goal"])

    def block(name: str, kcal: int, ideas: list[str]) -> str:
        return f"<b>{name}</b> — ~{kcal} ккал\n▫️ " + "\n▫️ ".join(ideas) + "\n"

    br = int(daily * 0.30)
    ln = int(daily * 0.40)
    dn = daily - br - ln

    text = "<b>Пример меню на день</b>\n\n"
    text += block("Завтрак", br, [
        "Овсянка на молоке + ягоды",
        "Яйца 2 шт + тост цельнозерновой",
        "Творог 5% + мёд/ягоды",
    ])
    text += block("Обед", ln, [
        "Куриная грудка + рис/гречка + салат",
        "Лосось + картофель + овощи",
        "Тофу/фасоль + киноа + овощи",
    ])
    text += block("Ужин", dn, [
        "Йогурт греческий + орехи + фрукты",
        "Омлет с овощами",
        "Тушёные овощи + индейка",
    ])
    text += "\nПодбери порции под свою норму калорий из /norms."
    await msg.answer(text)
