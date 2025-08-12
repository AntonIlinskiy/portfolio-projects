from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.keyboards import main_menu

router = Router()

class CalcFSM(StatesGroup):
    area = State()
    repair_type = State()
    finish = State()

BTN_BACK = KeyboardButton(text="🔙 Назад")
BTN_MAIN = KeyboardButton(text="⬅️ Возврат в главное меню")

def type_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Косметический"), KeyboardButton(text="Капитальный")],
            [BTN_BACK], [BTN_MAIN]
        ],
        resize_keyboard=True
    )

def finish_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Базовый"), KeyboardButton(text="Стандарт"), KeyboardButton(text="Премиум")],
            [BTN_BACK], [BTN_MAIN]
        ],
        resize_keyboard=True
    )

@router.message(F.text == "🧮 Калькулятор")
async def calc_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите площадь помещения в м² (например: 54):", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[BTN_BACK], [BTN_MAIN]],
        resize_keyboard=True
    ))
    await state.set_state(CalcFSM.area)

@router.message(CalcFSM.area, F.text.regexp(r"^\d{1,4}$"))
async def calc_set_area(message: Message, state: FSMContext):
    area = int(message.text)
    if area == 0:
        await message.answer("Площадь не может быть 0. Введите число в м²:")
        return
    await state.update_data(area=area)
    await message.answer("Выберите тип ремонта:", reply_markup=type_kb())
    await state.set_state(CalcFSM.repair_type)

@router.message(CalcFSM.area)
async def calc_area_invalid(message: Message):
    await message.answer("Пожалуйста, введите число (м²), например: 42")

@router.message(CalcFSM.repair_type, F.text.in_(["Косметический", "Капитальный"]))
async def calc_set_type(message: Message, state: FSMContext):
    await state.update_data(repair_type=message.text)
    await message.answer("Выберите уровень отделки:", reply_markup=finish_kb())
    await state.set_state(CalcFSM.finish)

@router.message(CalcFSM.repair_type, F.text == "🔙 Назад")
async def calc_back_from_type(message: Message, state: FSMContext):
    await state.set_state(CalcFSM.area)
    await message.answer("Введите площадь помещения в м²:")

@router.message(CalcFSM.finish, F.text.in_(["Базовый", "Стандарт", "Премиум"]))
async def calc_set_finish(message: Message, state: FSMContext):
    await state.update_data(finish=message.text)
    data = await state.get_data()
    area = data["area"]
    repair_type = data["repair_type"]
    finish = data["finish"]

    # Базовые ставки (руб/м²) — просто пример, поправим легко
    base = 2200 if repair_type == "Косметический" else 4500
    k_finish = {"Базовый": 1.0, "Стандарт": 1.25, "Премиум": 1.6}[finish]

    work = int(base * k_finish * area)
    materials = int(work * 0.45)           # прикидка материалов (45% от работ)
    management = int(work * 0.07)          # ведение проекта
    total = work + materials + management

    text = (
        "📐 Предварительный расчёт\n\n"
        f"Площадь: {area} м²\n"
        f"Тип ремонта: {repair_type}\n"
        f"Отделка: {finish}\n\n"
        f"Работы: {work:,} ₽\n"
        f"Материалы: {materials:,} ₽\n"
        f"Управление проектом: {management:,} ₽\n"
        f"— — — — — — — — — —\n"
        f"Итого: {total:,} ₽\n\n"
        "⚠️ Это ориентировочная смета. Для точного расчёта оставьте заявку."
    ).replace(",", " ")

    await state.clear()
    await message.answer(text, reply_markup=main_menu())

@router.message(CalcFSM.finish, F.text == "🔙 Назад")
async def calc_back_from_finish(message: Message, state: FSMContext):
    await state.set_state(CalcFSM.repair_type)
    await message.answer("Выберите тип ремонта:", reply_markup=type_kb())

@router.message(F.text == "⬅️ Возврат в главное меню")
async def calc_back_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 Главное меню", reply_markup=main_menu())
