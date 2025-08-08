from aiogram import Router, F
from aiogram.types import Message, FSInputFile

router = Router()

@router.message(F.text == "📁 Портфолио")
async def show_portfolio(message: Message):
    # Отправка 3 изображений
    photo1 = FSInputFile("data/portfolio/design.png")      # Проектирование
    photo2 = FSInputFile("data/portfolio/repair.png")      # Ремонт
    photo3 = FSInputFile("data/portfolio/construction.png")  # Строительство

    await message.answer_photo(photo=photo1, caption="📐 Проектирование домов")
    await message.answer_photo(photo=photo2, caption="🛠 Ремонт квартир под ключ")
    await message.answer_photo(photo=photo3, caption="🏡 Строительство домов")

    # Добавим ссылку на сайт
    await message.answer("📁 Наше портфолио:\nhttps://ваш_сайт.tilda.ws")
