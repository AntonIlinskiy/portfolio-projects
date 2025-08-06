from aiogram import Router, types
from services.car_cost_service import get_final_car_cost

router = Router()

@router.message()
async def handle_link(message: types.Message):
    text = message.text

    if "avito.ru" in text or "drom.ru" in text:
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
        await message.answer("📎 Пожалуйста, отправьте ссылку на Avito или Drom.")
