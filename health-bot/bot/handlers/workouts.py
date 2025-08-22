import logging
import calendar
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

from bot.services.gym_workouts import get_gym_plan
from bot.storage.db import SessionLocal
from bot.storage.crud import add_workout_log, get_recent_logs, get_streak_days, undo_today_log

router = Router()

def workouts_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="📋 План на неделю", callback_data="wk:plan")
    kb.button(text="🔥 Тренировка сегодня", callback_data="wk:today")
    kb.button(text="✅ Отметить выполнено", callback_data="wk:done")
    kb.adjust(1)
    return kb.as_markup()

def back_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data="wk:back")
    return kb.as_markup()

def format_day(day_num: int, block: dict) -> str:
    txt = f"<b>День {day_num}: {block['title']}</b>\n"
    for ex in block["exercises"]:
        txt += f"▫️ {ex['name']} — {ex['sets']}×{ex['reps']}\n"
    return txt

def format_full_plan(plan: dict) -> str:
    days_count = len(plan) if isinstance(plan, dict) else 0
    text = f"🏋️‍♂️ <b>План тренировок (зал, {days_count} дней)</b>\n\n"
    for day in sorted(plan.keys()):
        text += format_day(day, plan[day]) + "\n"
    text += "Совет: делай 1–2 разминочных подхода, отдых 60–120 сек.\n"
    return text

async def safe_edit(cb: CallbackQuery, new_text: str, markup):
    try:
        current_text = cb.message.html_text or cb.message.text or ""
        if current_text == new_text:
            await cb.answer("Уже актуально ✅", show_alert=False)
            return
        await cb.message.edit_text(new_text, reply_markup=markup)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e).lower():
            await cb.answer("Уже актуально ✅", show_alert=False)
        else:
            logging.exception("edit error", exc_info=e)
            await cb.message.answer(f"❌ Ошибка: <code>{type(e).__name__}: {e}</code>")
    except Exception as e:
        logging.exception("edit error", exc_info=e)
        await cb.message.answer(f"❌ Ошибка: <code>{type(e).__name__}: {e}</code>")

@router.message(Command("history"))
async def history_cmd(msg: Message):
    db = SessionLocal()
    try:
        rows = get_recent_logs(db, msg.from_user.id, limit=10)
        if not rows:
            await msg.answer("История пуста. Нажимай «✅ Отметить выполнено» после тренировки.")
            return
        lines = ["<b>Последние тренировки</b>"]
        for r in rows:
            dt = r.performed_at.strftime("%d.%m %H:%M") if hasattr(r.performed_at, "strftime") else str(r.performed_at)
            title = r.title or "Тренировка"
            day = f" (день {r.day})" if r.day else ""
            lines.append(f"• {dt} — {title}{day}")
            await msg.answer("\n".join(lines))
    finally:
        db.close()

@router.message(Command("streak"))
async def streak_cmd(msg: Message):
    db = SessionLocal()
    try:
        s = get_streak_days(db, msg.from_user.id)
        fire = "🔥" if s >= 3 else "💪" if s >= 1 else "🙂"
        await msg.answer(f"{fire} Твой текущий стрик: <b>{s}</b> дн.")
    finally:
        db.close()

@router.message(Command("undo"))
async def undo_cmd(msg: Message):
    db = SessionLocal()
    try:
        ok = undo_today_log(db, msg.from_user.id)
    finally:
        db.close()
    if ok:
        await msg.answer("↩️ Последняя отметка за сегодня отменена.")
    else:
        await msg.answer("Сегодня ещё нет отметок, отменять нечего.")              

@router.message(Command("workout"))
async def workout_entry(msg: Message):
    await msg.answer(
        "Раздел тренировки. Выбери действие:",
        reply_markup=workouts_menu_kb(),
    )

@router.callback_query(F.data == "wk:plan")
async def cb_plan(cb: CallbackQuery):
    plan = get_gym_plan("mass", 7)
    text = format_full_plan(plan)
    await cb.message.answer(text, reply_markup=back_kb())
    await cb.answer()

@router.callback_query(F.data == "wk:back")
async def cb_back(cb: CallbackQuery):
    await safe_edit(cb, "Раздел тренировки. Выбери действие:", workouts_menu_kb())
    await cb.answer()

@router.callback_query(F.data == "wk:today")
async def cb_today(cb: CallbackQuery):
    wd = datetime.now().weekday()   
    day = wd + 1
    plan = get_gym_plan("mass", 7)
    block = plan.get(day)
    week_day_name = calendar.day_name[wd]
    txt = f"Сегодня {week_day_name}.\n" + (format_day(day, block) if block else "Отдых.")
    await safe_edit(cb, txt, workouts_menu_kb())
    await cb.answer()

@router.callback_query(F.data == "wk:done")
async def cb_done(cb: CallbackQuery):
    wd = datetime.now().weekday()
    day = wd + 1
    plan = get_gym_plan("mass", 7)
    title = (plan.get(day) or {}).get("title") if isinstance(plan, dict) else None

    db = SessionLocal()
    try:
        add_workout_log(db, cb.from_user.id, day=day, title=title)
    finally:
        db.close()

    await cb.answer("Круто! Отмечено как выполнено 💪", show_alert=True)

@router.message(Command("gym"))
async def gym_cmd(msg: Message):
    plan = get_gym_plan("mass, 7")
    text = format_full_plan(plan)
    await msg.answer(text, reply_markup=back_kb())    
