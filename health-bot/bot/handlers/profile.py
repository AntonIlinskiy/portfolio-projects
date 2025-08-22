# bot/handlers/profile.py
import re
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.states import ProfileForm
from bot.storage.db import SessionLocal
from bot.storage import crud
from bot.services.nutrition import bmr_mifflin, tdee, target_kcal, macros_for

router = Router()

# Временное RAM-хранилище (MVP)
USERS: dict[int, dict] = {}

# --- Клавиатуры ---
def kb_sex():
    kb = InlineKeyboardBuilder()
    kb.button(text="Мужской", callback_data="sex:male")
    kb.button(text="Женский", callback_data="sex:female")
    kb.adjust(2)
    return kb.as_markup()

def kb_goal():
    kb = InlineKeyboardBuilder()
    kb.button(text="Похудение", callback_data="goal:lose")
    kb.button(text="Поддержание", callback_data="goal:maintain")
    kb.button(text="Набор массы", callback_data="goal:gain")
    kb.adjust(1)
    return kb.as_markup()

def kb_activity():
    kb = InlineKeyboardBuilder()
    kb.button(text="Сидячий", callback_data="act:sedentary")
    kb.button(text="Лёгкая", callback_data="act:light")
    kb.button(text="Средняя", callback_data="act:moderate")
    kb.button(text="Активная", callback_data="act:active")
    kb.button(text="Очень активная", callback_data="act:very_active")
    kb.adjust(1)
    return kb.as_markup()

def kb_diet():
    kb = InlineKeyboardBuilder()
    kb.button(text="Обычное", callback_data="diet:regular")
    kb.button(text="Вегетарианское", callback_data="diet:vegetarian")
    kb.button(text="Кето", callback_data="diet:keto")
    kb.adjust(1)
    return kb.as_markup()

def kb_confirm():
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Подтвердить", callback_data="confirm:yes")
    kb.button(text="✏️ Изменить", callback_data="confirm:no")
    kb.adjust(2)
    return kb.as_markup()

# --- Валидация ---
def parse_int(msg: str, min_v: int, max_v: int) -> int | None:
    if not re.fullmatch(r"\d{1,3}", msg.strip()):
        return None
    v = int(msg)
    return v if min_v <= v <= max_v else None

def parse_float(msg: str, min_v: float, max_v: float) -> float | None:
    m = re.fullmatch(r"\d{2,3}([.,]\d{1,2})?", msg.strip())
    if not m:
        return None
    v = float(msg.replace(",", "."))
    return v if min_v <= v <= max_v else None

def profile_text(data: dict) -> str:
    map_goal = {"lose":"Похудение","maintain":"Поддержание","gain":"Набор массы"}
    map_sex = {"male":"Муж","female":"Жен"}
    map_act = {
        "sedentary":"Сидячий","light":"Лёгкая","moderate":"Средняя",
        "active":"Активная","very_active":"Очень активная"
    }
    map_diet = {"regular":"Обычное","vegetarian":"Вегетарианское","keto":"Кето"}

    return (
        "<b>Профиль</b>\n"
        f"Имя: {data.get('name','—')}\n"
        f"Пол: {map_sex.get(data.get('sex'),'—')}\n"
        f"Возраст: {data.get('age','—')}\n"
        f"Рост: {data.get('height','—')} см\n"
        f"Вес: {data.get('weight','—')} кг\n"
        f"Цель: {map_goal.get(data.get('goal'),'—')}\n"
        f"Активность: {map_act.get(data.get('activity'),'—')}\n"
        f"Тип питания: {map_diet.get(data.get('diet'),'—')}\n"
        f"Аллергии/ограничения: {data.get('allergies','нет') or 'нет'}\n"
    )

@router.message(Command("profile"))
async def start_profile(msg: Message, state: FSMContext):
    await state.set_state(ProfileForm.name)
    await msg.answer("Как тебя зовут?")

@router.callback_query(F.data == "menu:profile")
async def menu_profile(cb: CallbackQuery, state: FSMContext):
    await state.set_state(ProfileForm.name)
    await cb.message.answer("Как тебя зовут?")
    await cb.answer()

@router.message(ProfileForm.name)
async def ask_sex(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text.strip()[:50])
    await state.set_state(ProfileForm.sex)
    await msg.answer("Выбери пол:", reply_markup=kb_sex())

@router.callback_query(ProfileForm.sex, F.data.startswith("sex:"))
async def set_sex(cb: CallbackQuery, state: FSMContext):
    _, sex = cb.data.split(":", 1)
    await state.update_data(sex=sex)
    await state.set_state(ProfileForm.age)
    await cb.message.answer("Сколько тебе лет? (число от 12 до 100)")
    await cb.answer()

@router.message(ProfileForm.age)
async def ask_height(msg: Message, state: FSMContext):
    age = parse_int(msg.text, 12, 100)
    if age is None:
        await msg.answer("Введи возраст числом, 12–100.")
        return
    await state.update_data(age=age)
    await state.set_state(ProfileForm.height)
    await msg.answer("Укажи рост в сантиметрах (например: 178)")

@router.message(ProfileForm.height)
async def ask_weight(msg: Message, state: FSMContext):
    height = parse_int(msg.text, 120, 230)
    if height is None:
        await msg.answer("Рост должен быть 120–230 см. Пример: 178")
        return
    await state.update_data(height=height)
    await state.set_state(ProfileForm.weight)
    await msg.answer("Укажи вес в кг (например: 76.5)")

@router.message(ProfileForm.weight)
async def ask_goal(msg: Message, state: FSMContext):
    weight = parse_float(msg.text, 30, 300)
    if weight is None:
        await msg.answer("Вес должен быть 30–300 кг. Пример: 76.5")
        return
    await state.update_data(weight=weight)
    await state.set_state(ProfileForm.goal)
    await msg.answer("Какая цель?", reply_markup=kb_goal())

@router.callback_query(ProfileForm.goal, F.data.startswith("goal:"))
async def set_goal(cb: CallbackQuery, state: FSMContext):
    _, goal = cb.data.split(":", 1)
    await state.update_data(goal=goal)
    await state.set_state(ProfileForm.activity)
    await cb.message.answer("Выбери уровень активности:", reply_markup=kb_activity())
    await cb.answer()

@router.callback_query(ProfileForm.activity, F.data.startswith("act:"))
async def set_activity(cb: CallbackQuery, state: FSMContext):
    _, act = cb.data.split(":", 1)
    await state.update_data(activity=act)
    await state.set_state(ProfileForm.diet)
    await cb.message.answer("Тип питания?", reply_markup=kb_diet())
    await cb.answer()

@router.callback_query(ProfileForm.diet, F.data.startswith("diet:"))
async def set_diet(cb: CallbackQuery, state: FSMContext):
    _, diet = cb.data.split(":", 1)
    await state.update_data(diet=diet)
    await state.set_state(ProfileForm.allergies)
    await cb.message.answer("Есть аллергии/ограничения? Напиши текстом (или «нет»).")
    await cb.answer()

@router.message(ProfileForm.allergies)
async def confirm(msg: Message, state: FSMContext):
    allergies = msg.text.strip()
    allergies = "" if allergies.lower() in {"нет","no","none","-"} else allergies[:200]
    await state.update_data(allergies=allergies)
    data = await state.get_data()
    await state.set_state(ProfileForm.confirm)
    await msg.answer(profile_text(data), reply_markup=kb_confirm())

@router.callback_query(ProfileForm.confirm, F.data.startswith("confirm:"))
async def finish(cb: CallbackQuery, state: FSMContext):
    _, choice = cb.data.split(":", 1)
    if choice == "no":
        await state.clear()
        await cb.message.answer("Ок, давай сначала. Как тебя зовут?")
        await state.set_state(ProfileForm.name)
        await cb.answer()
        return

    data = await state.get_data()
    USERS[cb.from_user.id] = data
    await state.clear()
    
    bmr = bmr_mifflin(data["sex"], int(data["age"]), float(data["height"]), float(data["weight"]))
    daily = target_kcal(tdee(bmr, data["activity"]), data["goal"])
    m = macros_for(daily, float(data["weight"]), data["goal"])

    db = SessionLocal()
    try:
        user = crud.get_or_create_user(db, cb.from_user.id)
        crud.update_user(
            db, user,
            name=data.get("name"),
            sex=data.get("sex"),
            age=int(data["age"]),
            height=float(data["height"]),
            weight=float(data["weight"]),
            goal=data.get("goal"),
            activity=data.get("activity"),
            diet=data.get("diet"),
            allergies=data.get("allergies") or "",
            kcal=m.kcal, protein_g=m.protein_g, fat_g=m.fat_g, carbs_g=m.carbs_g,
        )
    finally:
        db.close()

    await cb.message.answer("Готово! Профиль сохранён ✅\n"
                            f"Твои нормы: {m.kcal} ккал / Б:{m.protein_g} Ж:{m.fat_g} У:{m.carbs_g}")
    await cb.answer()