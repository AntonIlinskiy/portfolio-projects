from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Анкета", callback_data="menu:profile")
    kb.button(text="🏋️‍♂️ Тренировки", callback_data="menu:workouts")
    kb.button(text="🍎 Питание", callback_data="menu:nutrition")
    kb.button(text="💳 Подписка", callback_data="menu:billing")
    kb.adjust(2)
    return kb.as_markup()

def main_menu_reply_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Анкета"), KeyboardButton(text="🏋️‍♂️ Тренировки")],
            [KeyboardButton(text="🍎 Питание"), KeyboardButton(text="💳 Подписка")],
        ],
        resize_keyboard=True
    )
