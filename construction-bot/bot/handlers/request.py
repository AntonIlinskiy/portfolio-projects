# bot/handlers/request.py
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()

# Клавиатуры
def cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )

def share_phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Поделиться номером", request_contact=True)],
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )

def main_kb():
    # если у тебя уже есть main_menu() — можно импортировать её вместо этой заглушки
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Услуги")],
            [KeyboardButton(text="📂 Портфолио")],
            [KeyboardButton(text="📝 Оставить заявку")]
        ],
        resize_keyboard=True
    )

class RequestForm(StatesGroup):
    name = State()
    phone = State()
    comment = State()

# Старт заявки
@router.message(F.text == "📝 Оставить заявку")
async def request_start(message: Message, state: FSMContext):
    await state.set_state(RequestForm.name)
    await message.answer("Как к вам обращаться?", reply_markup=cancel_kb())

# Имя → телефон
@router.message(RequestForm.name, F.text.len() > 1)
async def request_got_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(RequestForm.phone)

    # попробуем взять телеграм-номер, если есть
    phone_hint = None
    if message.from_user and message.from_user.username:
        phone_hint = f"@{message.from_user.username}"

    text = "Отправьте номер телефона (или нажмите кнопку «Поделиться номером»)."
    if phone_hint:
        text += f"\n(Можем связаться и через Telegram: {phone_hint})"

    await message.answer(text, reply_markup=share_phone_kb())

# Телефон: через контакт
@router.message(RequestForm.phone, F.contact)
async def request_got_contact(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(RequestForm.comment)
    await message.answer("Коротко опишите задачу:", reply_markup=cancel_kb())

# Телефон: вручную
@router.message(RequestForm.phone, F.text)
async def request_got_phone_text(message: Message, state: FSMContext):
    raw = message.text.strip()
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) < 10:
        await message.answer("Похоже на неверный номер. Укажите в формате +7XXXXXXXXXX или поделитесь контактом.")
        return
    if not raw.startswith("+"):
        raw = "+" + digits
    await state.update_data(phone=raw)
    await state.set_state(RequestForm.comment)
    await message.answer("Коротко опишите задачу:", reply_markup=cancel_kb())

# Комментарий → финал
@router.message(RequestForm.comment, F.text)
async def request_finish(message: Message, state: FSMContext):
    await state.update_data(comment=message.text.strip())
    data = await state.get_data()
    await state.clear()

    # сюда можно подставить ID админа, чтобы отправлять заявку в личку
    text = (
        "✅ Заявка отправлена!\n\n"
        f"Имя: {data.get('name')}\n"
        f"Телефон: {data.get('phone')}\n"
        f"Комментарий: {data.get('comment')}"
    )
    await message.answer(text, reply_markup=main_kb())

# Отмена
@router.message(F.text == "❌ Отмена")
async def request_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Отменено. Возвращаю в главное меню.", reply_markup=main_kb())
