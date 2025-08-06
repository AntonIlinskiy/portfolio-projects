import asyncio
from aiogram import Bot, Dispatcher
from bot.config import load_config
from bot.handlers import start, link_handler

async def main():
    config = load_config()
    bot = Bot(token=config["BOT_TOKEN"])
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(link_handler.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
