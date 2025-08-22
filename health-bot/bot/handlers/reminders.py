import re
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from bot.storage.db import SessionLocal
from bot.storage.crud import (
    get_reminders_for_user, set_water_reminder, upsert_workout_reminder
)
from bot.services.scheduler import schedule_user_reminders

router = Router()

def _format_status(rows) -> str:
    water = next((r for r in rows if r.kind == 'water'), None)
    workout = next((r for r in rows if r.kind == 'workout'), None)
    wtxt = "вкл (10.00-20.00 каждые два часа)" if water and water.enabled else "выкл"
    ttxt = f"в {workout.time_str}" if workout and workout.enabled and workout.time_str else "не задано"
    return (
        "<b>Напоминания</b>\n"
        f"💧 Вода: {wtxt}\n"
        f"🏋️ Тренировка: {ttxt}\n\n"
        "Команды:\n"
        "• /water_on — включить воду\n"
        "• /water_off — выключить воду\n"
        "• /setworkout HH:MM — время тренировки (например, /setworkout 19:00)\n"
        "• /unsetworkout — убрать время тренировки\n"
    )

@router.message(Command("reminders"))
async def reminders_status(msg: Message):
    db = SessionLocal()
    try:
        rows = get_reminders_for_user(db, msg.from_user.id)
        await msg.answer(_format_status(rows))
    finally:
        db.close()

@router.message(Command("water_on"))
async def water_on(msg: Message):
    db = SessionLocal()
    try:
        set_water_reminder(db, msg.from_user.id, True)
        from bot.storage.crud import get_reminders_for_user
        from bot.services.scheduler import scheduler
        rows = get_reminders_for_user(db, msg.from_user.id)
        schedule_user_reminders(msg.bot, msg.from_user.id, rows)
        await msg.answer("💧 Напоминание о воде включено (каждые 2 часа с 10:00 до 20:00).")
    finally:
        db.close()
                           
    
@router.message(Command("water_off"))
async def water_off(msg: Message):
    db = SessionLocal()
    try:
        set_water_reminder(db, msg.from_user.id, False)
        rows = get_reminders_for_user(db, msg.from_user.id)
        schedule_user_reminders(msg.bot, msg.from_user.id, rows)
        await msg.answer("💧 Напоминание о воде выключено.")
    finally:
        db.close()

@router.message(Command("setworkout"))
async def set_workout(msg: Message, command: CommandObject):
    arg = (command.args or "").strip()
    if not re.fullmatch(r"\d{1,2}:\d{2}", arg):
        await msg.answer("Укажи время в формате HH:MM. Пример: /setworkout 19:00")
        return
    hh, mm = arg.split(":")
    if not (0 <= int(hh) <= 23 and 0 <= int(mm) <= 59):
        await msg.answer("Некорректное время. Пример: /setworkout 19:00")
        return
    db = SessionLocal()
    try:
        upsert_workout_reminder(db, msg.from_user.id, f"{int(hh):02d}:{int(mm):02d}")
        rows = get_reminders_for_user(db, msg.from_user.id)
        schedule_user_reminders(msg.bot, msg.from_user.id, rows)
        await msg.answer(f"🏋️ Напоминание о тренировке установлено на {int(hh):02d}:{int(mm):02d} ежедневно.")
    finally:
        db.close()        

@router.message(Command("unsetworkout"))
async def unset_workout(msg: Message):
    db = SessionLocal()
    try:
        upsert_workout_reminder(db, msg.from_user.id, None)
        rows = get_reminders_for_user(db, msg.from_user.id)
        schedule_user_reminders(msg.bot, msg.from_user.id, rows)
        await msg.answer("🏋️ Напоминание о тренировке отключено.")
    finally:
        db.close()      