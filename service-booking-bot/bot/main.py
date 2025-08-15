import asyncio, os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from bot.handlers import router as handlers_router
from services.repo import init_db   

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN отсутствует в .env")

    init_db()  

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
