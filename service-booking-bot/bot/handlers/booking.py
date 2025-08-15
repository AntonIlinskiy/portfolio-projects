from datetime import date, timedelta
from aiogram import Router, F
from aiogram.types import (
    Message, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.slots import get_free_slots, reserve_slot



try:
    from bot.keyboards import main_menu
except Exception:
    main_menu = None

router = Router()




class BookingForm(StatesGroup):
    service = State()
    brand   = State()
    model   = State()
    date    = State()
    time    = State()



def generate_dates(days: int = 7) -> list[str]:
    """Список дат на ближайшие N дней в формате YYYY-MM-DD."""
    today = date.today()
    return [(today + timedelta(days=i)).isoformat() for i in range(days)]


def services_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Замена масла"), KeyboardButton(text="ТО")],
            [KeyboardButton(text="Диагностика"), KeyboardButton(text="Шиномонтаж")],
            [KeyboardButton(text="✖️ Отмена")],
        ],
        resize_keyboard=True
    )


def cancel_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✖️ Отмена")]],
        resize_keyboard=True
    )


def dates_inline_kb(dates: list[str]) -> InlineKeyboardMarkup:
    rows = []
    row = []
    for i, d in enumerate(dates, start=1):
        row.append(InlineKeyboardButton(text=d, callback_data=f"date:{d}"))
        if i % 3 == 0:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def times_inline_kb(times: list[str]) -> InlineKeyboardMarkup:
    rows = []
    row = []
    for i, t in enumerate(times, start=1):
        row.append(InlineKeyboardButton(text=t, callback_data=f"time:{t}"))
        if i % 4 == 0:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)



@router.message(F.text == "🗓 Записаться на ТО")
async def start_booking(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(BookingForm.service)
    await message.answer(
        "Выберите услугу:",
        reply_markup=services_kb()
    )



@router.message(BookingForm.service, F.text)
async def set_service(message: Message, state: FSMContext):
    text = message.text.strip()
    if text == "✖️ Отмена":
        await state.clear()
        await message.answer("Отменено.", reply_markup=ReplyKeyboardRemove())
        if main_menu:
            await message.answer("🏠 Главное меню", reply_markup=main_menu())
        return

    await state.update_data(service=text)
    await state.set_state(BookingForm.brand)
    await message.answer(
        "Введите марку автомобиля (например: BMW):",
        reply_markup=cancel_kb()
    )



@router.message(BookingForm.brand, F.text)
async def set_brand(message: Message, state: FSMContext):
    text = message.text.strip()
    if text == "✖️ Отмена":
        await state.clear()
        await message.answer("Отменено.", reply_markup=ReplyKeyboardRemove())
        if main_menu:
            await message.answer("🏠 Главное меню", reply_markup=main_menu())
        return

    await state.update_data(brand=text)
    await state.set_state(BookingForm.model)
    await message.answer(
        "Введите модель (например: X5):",
        reply_markup=cancel_kb()
    )



@router.message(BookingForm.model, F.text)
async def set_model(message: Message, state: FSMContext):
    text = message.text.strip()
    if text == "✖️ Отмена":
        await state.clear()
        await message.answer("Отменено.", reply_markup=ReplyKeyboardRemove())
        if main_menu:
            await message.answer("🏠 Главное меню", reply_markup=main_menu())
        return

    await state.update_data(model=text)
    await state.set_state(BookingForm.date)

    ds = generate_dates(7)
    await message.answer(
        "Выберите дату:",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "Ближайшие доступные дни:",
        reply_markup=dates_inline_kb(ds)
    )



@router.callback_query(F.data.startswith("date:"))
async def pick_date_cb(callback: CallbackQuery, state: FSMContext):
    _, picked = callback.data.split(":", 1)
    await state.update_data(date=picked)

    
    slots = get_free_slots(picked) or []
    if not slots:
        await callback.answer("На эту дату свободных слотов нет.", show_alert=True)
       
        ds = generate_dates(7)
        await callback.message.edit_text("Выберите другую дату:")
        await callback.message.edit_reply_markup(reply_markup=dates_inline_kb(ds))
        return

    await state.set_state(BookingForm.time)
    await callback.message.edit_text(f"Дата: {picked}\nВыберите время:")
    await callback.message.edit_reply_markup(reply_markup=times_inline_kb(slots))



@router.callback_query(F.data.startswith("time:"))
async def pick_time_cb(callback: CallbackQuery, state: FSMContext):
    
    try:
        _, time_str = callback.data.split(":", 1)
    except Exception:
        await callback.answer("Некорректное время.", show_alert=True)
        return

    data = await state.get_data()
    date_str = data.get("date")
    service  = data.get("service")
    brand    = data.get("brand")
    model    = data.get("model")
    user_id  = callback.from_user.id

    if not date_str:
        await callback.answer("Сначала выберите дату.", show_alert=True)
        return
    if not all([service, brand, model]):
        await callback.answer("Не хватает данных (услуга/марка/модель). Начните заново.", show_alert=True)
        await state.clear()
        return

    ok = reserve_slot(date_str, time_str, user_id, service, brand, model)
    if not ok:
        await callback.answer("Этот слот только что заняли. Выберите другое время.", show_alert=True)
        # Обновим список доступных слотов на эту же дату
        slots = get_free_slots(date_str) or []
        if not slots:
            await callback.message.edit_text("К сожалению, на эту дату свободных слотов больше нет.")
            return
        await callback.message.edit_reply_markup(reply_markup=times_inline_kb(slots))
        return

    await callback.message.edit_text(
        "✅ Запись подтверждена!\n\n"
        f"Услуга: {service}\n"
        f"Авто: {brand} {model}\n"
        f"Дата: {date_str}\n"
        f"Время: {time_str}"
    )
    await state.clear()



@router.message(F.text == "✖️ Отмена")
async def cancel_flow(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Отменено.", reply_markup=ReplyKeyboardRemove())
    if main_menu:
        await message.answer("🏠 Главное меню", reply_markup=main_menu())
