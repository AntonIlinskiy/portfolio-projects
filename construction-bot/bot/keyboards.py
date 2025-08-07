from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏗 Услуги")],
            [KeyboardButton(text="📁 Портфолио")],
        ],
        resize_keyboard=True
    )
