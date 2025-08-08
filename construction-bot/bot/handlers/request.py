from aiogram import Router, F
from aiogram.types import Message, Contact, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class RequestForm(StatesGroup):
    waiting_for_description = State()

# Портфолио
@router.message(F.text == "📁 Портфолио")
async def handle_portfolio(message: Message):
    await message.answer("📁 Наше портфолио:\nhttps://ваш_сайт.tilda.ws")

# Контакт
@router.message(F.contact)
async def handle_contact(message: Message, state: FSMContext):
    contact = message.contact
    await state.update_data(phone=contact.phone_number)

    await message.answer(
        "✍️ Спасибо! Теперь, пожалуйста, напишите, что вас интересует.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(RequestForm.waiting_for_description)

# Описание заявки
@router.message(RequestForm.waiting_for_description)
async def handle_description(message: Message, state: FSMContext):
    data = await state.get_data()
    phone = data.get("phone", "не указан")

    admin_id = message.from_user.id  # или свой id
    await message.bot.send_message(
        admin_id,
        f"📨 Новая заявка:\nТелефон: {phone}\nСообщение: {message.text}"
    )

    await message.answer("✅ Заявка принята, скоро мы с вами свяжемся!")
    await state.clear()


