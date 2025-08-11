# bot/handlers/portfolio.py
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InputMediaPhoto

router = Router()

@router.message(F.text == "📁 Портфолио")
async def portfolio(message: Message):
    # пути к локальным изображениям
    base = "bot/data/portfolio/"
    imgs = [
        FSInputFile(base + "design.png"),
        FSInputFile(base + "repair.png"),
        FSInputFile(base + "construction.jpg"),
    ]

    # альбом (media-group) — минимум 2, максимум 10
    media = [
        InputMediaPhoto(media=imgs[0], caption="Примеры наших работ: дизайн, ремонт и строительство."),
        InputMediaPhoto(media=imgs[1]),
        InputMediaPhoto(media=imgs[2]),
    ]

    await message.answer("🖼 Наше портфолио (3 примера):")
    await message.answer_media_group(media)
