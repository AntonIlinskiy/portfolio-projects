from aiogram import Router, types
from services.car_cost_service import get_final_car_cost
from urllib.parse import urlparse

router = Router()

def is_valid_avito_url(url: str) -> bool:
    parsed = urlparse(url)
    return (
        "avito.ru" in parsed.netloc and
        "/avtomobili/" in parsed.path
    )

def is_valid_drom_url(url: str) -> bool:
    parsed = urlparse(url)
    return "drom.ru" in parsed.netloc and "/cars/" in parsed.path

@router.message()
async def handle_link(message: types.Message):
    text = message.text.strip()

    if is_valid_avito_url(text) or is_valid_drom_url(text):
        await message.answer("⏳ Пытаюсь получить информацию по ссылке...")

        result = get_final_car_cost(text)
        if not result:
            await message.answer("❌ Не удалось получить информацию о машине")
            return

        await message.answer(
            f"🚗 Рассчитанная стоимость авто:\n\n"
            f"Цена на сайте: {result['base_price']} ₽\n"
            f"Доставка: {result['delivery_cost']} ₽\n"
            f"Таможня: {result['customs_fee']} ₽\n"
            f"Услуги: {result['service_fee']} ₽\n\n"
            f"💰 Итого: {result['total_cost']} ₽"
        )
    else:
        await message.answer("📎 Пожалуйста, отправьте корректную ссылку на авто с Avito или Drom.")
