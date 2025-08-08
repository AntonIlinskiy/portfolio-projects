from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏗 Услуги")],
            [KeyboardButton(text="📁 Портфолио")],
            [KeyboardButton(text="📝 Оставить заявку", request_contact=True)]
        ],
        resize_keyboard=True
    )

def services_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📐 Проектирование домов")],
            [KeyboardButton(text="🛠 Ремонт квартир под ключ")],
            [KeyboardButton(text="🏡 Строительство домов")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
