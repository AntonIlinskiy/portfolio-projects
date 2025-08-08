import asyncio
from aiogram import Bot, Dispatcher
from bot.config import TOKEN
from bot.handlers import start
from bot.handlers.services import router as services_router
from bot.handlers.request import router as request_router
from bot.handlers import start, services, request
from bot.handlers import portfolio


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(start.router)
    dp.include_router(services_router)
    dp.include_router(request.router)
    dp.include_router(portfolio.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
