from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import re

router = Router()

# --- Кнопки ---
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
    resize_keyboard=True
)

back_cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[BTN_BACK, BTN_CANCEL]],
    resize_keyboard=True
)

phone_kb = ReplyKeyboardMarkup(
    keyboard=[[BTN_SHARE_PHONE], [BTN_BACK, BTN_CANCEL]],
    resize_keyboard=True
)

# --- Состояния формы ---
class RequestForm(StatesGroup):
    name = State()
    phone = State()
    service = State()
    comment = State()
    confirm = State()

# --- Старт формы ---
@router.message(F.text == "📞 Оставить заявку")
async def request_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(RequestForm.name)
    await message.answer(
        "Давайте оформим заявку.\n\nКак к вам обращаться?",
        reply_markup=back_cancel_kb
    )

# --- Имя ---
@router.message(RequestForm.name, F.text)
async def req_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Имя слишком короткое. Введите, пожалуйста, ещё раз.", reply_markup=back_cancel_kb)
        return
    await state.update_data(name=name)
    await state.set_state(RequestForm.phone)
    await message.answer(
        "Отправьте номер телефона (в формате +7XXXXXXXXXX) или нажмите кнопку «📱 Отправить номер».",
        reply_markup=phone_kb
    )

# --- Телефон: контакт из Telegram ---
@router.message(RequestForm.phone, F.contact)
async def req_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await state.set_state(RequestForm.service)
    await message.answer("Какой тип услуги нужен?", reply_markup=services_kb)

# --- Телефон: текстом ---
PHONE_RE = re.compile(r"^\+?\d{10,15}$")

@router.message(RequestForm.phone, F.text)
async def req_phone_text(message: Message, state: FSMContext):
    phone = message.text.strip().replace(" ", "")
    if not PHONE_RE.match(phone):
        await message.answer("Не похоже на номер телефона. Введите в формате +7XXXXXXXXXX или отправьте контакт.", reply_markup=phone_kb)
        return
    await state.update_data(phone=phone)
    await state.set_state(RequestForm.service)
    await message.answer("Какой тип услуги нужен?", reply_markup=services_kb)

# --- Выбор услуги ---
@router.message(RequestForm.service, F.text.in_({
    "🛠 Ремонт квартир под ключ",
    "🏡 Строительство домов",
    "📐 Проектирование домов"
}))
async def req_service(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await state.set_state(RequestForm.comment)
    await message.answer("Коротко опишите задачу (необязательно). Можете просто отправить «—».", reply_markup=back_cancel_kb)

# --- Комментарий ---
@router.message(RequestForm.comment, F.text)
async def req_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text.strip())
    data = await state.get_data()

    summary = (
        "✅ Заявка собрана:\n\n"
        f"Имя: {data.get('name')}\n"
        f"Телефон: {data.get('phone')}\n"
        f"Услуга: {data.get('service')}\n"
        f"Комментарий: {data.get('comment') or '—'}\n\n"
        "Отправляю администратору. Спасибо!"
    )
    await message.answer(summary, reply_markup=ReplyKeyboardRemove())

    # TODO: сюда поставь ID администратора или chat_id, куда слать заявки
    ADMIN_CHAT_ID = None  # например, 123456789
    if ADMIN_CHAT_ID:
        try:
            await message.bot.send_message(
                ADMIN_CHAT_ID,
                f"📥 Новая заявка:\n"
                f"Имя: {data.get('name')}\n"
                f"Телефон: {data.get('phone')}\n"
                f"Услуга: {data.get('service')}\n"
                f"Комментарий: {data.get('comment') or '—'}"
            )
        except Exception as e:
            await message.answer(f"⚠️ Не удалось переслать заявку админу: {e}")

    await state.clear()
    # вернём главное меню (импортируй при желании main_menu)
    try:
        from bot.keyboards import main_menu
        await message.answer("🏠 Главное меню", reply_markup=main_menu())
    except Exception:
        pass

# --- Универсальные: отмена и возврат ---
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
