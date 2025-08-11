import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import TOKEN

# импортируем именно router из каждого файла и даём имена
from bot.handlers.start import router as start_router
from bot.handlers.services import router as services_router
from bot.handlers.request import router as request_router
from bot.handlers.portfolio import router as portfolio_router

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(services_router)
    dp.include_router(request_router)
    dp.include_router(portfolio_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
