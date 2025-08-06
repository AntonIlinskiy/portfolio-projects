from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот, который помогает рассчитать полную стоимость автомобиля с Avito.\n\n"
        "🚗 Просто пришли мне ссылку на объявление с сайта Avito, "
        "и я посчитаю стоимость машины с учётом:\n"
        "- доставки\n"
        "- таможни\n"
        "- услуг по оформлению\n\n"
        "Готов? Отправь ссылку! 🔗"
    )
