# bot/handlers/request.py
from __future__ import annotations

import re
from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from services.gsheets import append_lead_row

router = Router()

# ==== Клавиатуры ====
BTN_BACK = KeyboardButton(text="⬅️ Возврат в главное меню")
BTN_CANCEL = KeyboardButton(text="✖️ Отмена")
BTN_SHARE_PHONE = KeyboardButton(text="📱 Отправить номер", request_contact=True)

services_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛠 Ремонт квартир под ключ")],
        [KeyboardButton(text="🏡 Строительство домов")],
        [KeyboardButton(text="📐 Проектирование домов")],
        [BTN_BACK, BTN_CANCEL],
    ],
    resize_keyboard=True,
)

back_cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[BTN_BACK, BTN_CANCEL]],
    resize_keyboard=True,
)

phone_kb = ReplyKeyboardMarkup(
    keyboard=[[BTN_SHARE_PHONE], [BTN_BACK, BTN_CANCEL]],
    resize_keyboard=True,
)

# ==== Состояния ====
class RequestForm(StatesGroup):
    name = State()
    phone = State()
    service = State()
    comment = State()

# ==== Старт ====
@router.message(F.text == "📞 Оставить заявку")
async def request_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(RequestForm.name)
    await message.answer(
        "Давайте оформим заявку.\n\nКак к вам обращаться?",
        reply_markup=back_cancel_kb,
    )

# ==== Имя ====
@router.message(RequestForm.name, F.text)
async def req_name(message: Message, state: FSMContext):
    name = (message.text or "").strip()
    if len(name) < 2:
        await message.answer("Имя слишком короткое. Введите, пожалуйста, ещё раз.", reply_markup=back_cancel_kb)
        return
    await state.update_data(name=name)
    await state.set_state(RequestForm.phone)
    await message.answer(
        "Отправьте номер телефона (в формате +7XXXXXXXXXX) или нажмите кнопку «📱 Отправить номер».",
        reply_markup=phone_kb,
    )

# ==== Телефон — контакт ====
@router.message(RequestForm.phone, F.contact)
async def req_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else ""
    await state.update_data(phone=phone)
    await state.set_state(RequestForm.service)
    await message.answer("Какой тип услуги нужен?", reply_markup=services_kb)

# ==== Телефон — текст ====
PHONE_RE = re.compile(r"^\+?\d{10,15}$")

@router.message(RequestForm.phone, F.text)
async def req_phone_text(message: Message, state: FSMContext):
    phone = (message.text or "").strip().replace(" ", "")
    if not PHONE_RE.match(phone):
        await message.answer(
            "Не похоже на номер телефона. Введите в формате +7XXXXXXXXXX или отправьте контакт.",
            reply_markup=phone_kb,
        )
        return
    await state.update_data(phone=phone)
    await state.set_state(RequestForm.service)
    await message.answer("Какой тип услуги нужен?", reply_markup=services_kb)

# ==== Выбор услуги ====
@router.message(
    RequestForm.service,
    F.text.in_({
        "🛠 Ремонт квартир под ключ",
        "🏡 Строительство домов",
        "📐 Проектирование домов",
    }),
)
async def req_service(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await state.set_state(RequestForm.comment)
    await message.answer(
        "Коротко опишите задачу (необязательно). Можете отправить «—».",
        reply_markup=back_cancel_kb,
    )

# ==== Комментарий + запись в Google Sheets ====
@router.message(RequestForm.comment, F.text)
async def req_comment(message: Message, state: FSMContext):
    comment = (message.text or "").strip()
    await state.update_data(comment=comment)

    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")
    service = data.get("service")
    username = message.from_user.username if message.from_user else None

    # Записываем в Google Sheets (через services.gsheets.append_lead_row)
    try:
        append_lead_row(
            when=datetime.now(),
            name=name,
            phone=phone,
            username=username,
            source="Telegram",
            service=service,
            comment=comment if comment and comment != "—" else "",
        )
    except Exception as e:
        await message.answer(f"⚠️ Не удалось записать в Google Sheets: {e}")

    # Подтверждение пользователю
    await message.answer(
        "✅ Заявка принята! Мы свяжемся с вами в ближайшее время.",
        reply_markup=ReplyKeyboardRemove(),
    )

    # Возврат в главное меню
    await state.clear()
    try:
        from bot.keyboards import main_menu
        await message.answer("🏠 Главное меню", reply_markup=main_menu())
    except Exception:
        pass

# ==== Отмена / Назад ====
@router.message(F.text == "✖️ Отмена")
async def req_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Отменено.", reply_markup=ReplyKeyboardRemove())
    try:
        from bot.keyboards import main_menu
        await message.answer("🏠 Главное меню", reply_markup=main_menu())
    except Exception:
        pass

@router.message(F.text == "⬅️ Возврат в главное меню")
async def req_back_to_main(message: Message, state: FSMContext):
    await state.clear()
    try:
        from bot.keyboards import main_menu
        await message.answer("🏠 Главное меню", reply_markup=main_menu())
    except Exception:
        await message.answer("🏠 Главное меню")
