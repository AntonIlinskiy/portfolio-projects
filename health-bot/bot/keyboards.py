from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Анкета", callback_data="menu:profile")
    kb.button(text="🏋️‍♂️ Тренировки", callback_data="menu:workouts")
    kb.button(text="🍎 Питание", callback_data="menu:nutrition")
    kb.button(text="💳 Подписка", callback_data="menu:billing")
    kb.adjust(2)
    return kb.as_markup()