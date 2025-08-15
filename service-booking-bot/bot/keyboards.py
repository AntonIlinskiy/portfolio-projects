from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓 Записаться на ТО")],
            [KeyboardButton(text="ℹ️ Услуги"), KeyboardButton(text="📞 Контакты")],
        ],
        resize_keyboard=True
    )

def back_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Назад в меню")],
        ],
        resize_keyboard=True
    )

def services_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ТО-1"), KeyboardButton(text="ТО-2")],
            [KeyboardButton(text="Диагностика"), KeyboardButton(text="Замена масла")],
            [KeyboardButton(text="⬅️ Назад в меню")],
        ],
        resize_keyboard=True
    )

def share_phone_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить номер", request_contact=True)],
            [KeyboardButton(text="⬅️ Назад в меню")],
        ],
        resize_keyboard=True
    )
