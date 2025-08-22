# bot/main.py
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from dotenv import load_dotenv # type: ignore

from bot.handlers import start, workouts, profile, nutrition, debug, reminders
from bot.storage.db import engine, SessionLocal
from bot.storage.models import Base, Reminder
from bot.services.scheduler import scheduler as JOBS, schedule_user_reminders

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN") or "8493785809:AAE_Pse4pQnYr8UlYYZXfyGUspma4WMpyWA"  

async def set_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать"),
        BotCommand(command="workout", description="Тренировки: меню"),
        BotCommand(command="gym", description="План зала (неделя)"),
        BotCommand(command="profile", description="Анкета пользователя"),
        BotCommand(command="norms", description="Мои нормы (ккал/БЖУ)"),
        BotCommand(command="menu", description="Пример меню на день"),
        BotCommand(command="reminders", description="Статус напоминаний"),
        BotCommand(command="water_on", description="Вода: включить"),
        BotCommand(command="water_off", description="Вода: выключить"),
        BotCommand(command="setworkout", description="Установить время тренировки"),
        BotCommand(command="unsetworkout", description="Убрать время тренировки"),
        BotCommand(command="history", description="История тренировок"),
        BotCommand(command="streak", description="Текущий стрик"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="ping", description="Проверка"),
    ])

async def main():
    Base.metadata.create_all(bind=engine)

    async with Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) as bot:
        dp = Dispatcher()

        # 3) роутеры
        dp.include_router(start.router)
        dp.include_router(workouts.router)
        dp.include_router(profile.router)
        dp.include_router(nutrition.router)
        dp.include_router(debug.router)
        dp.include_router(reminders.router)

        if not JOBS.running:
            JOBS.start()

        db = SessionLocal()
        try:
            tg_ids = {r.tg_id for r in db.query(Reminder).all()}
            for tg_id in tg_ids:
                rows = db.query(Reminder).filter(Reminder.tg_id == tg_id).all()
                schedule_user_reminders(bot, tg_id, rows)
        finally:
            db.close()

        await set_commands(bot)
        print("Bot started...")

        try:
            await dp.start_polling(bot)
        finally:
           JOBS.shutdown(wait=False)

if __name__ == "__main__":
    asyncio.run(main())
