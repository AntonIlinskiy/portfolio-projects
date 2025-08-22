# bot/handlers/start.py (фрагмент)
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards import main_menu_kb

router = Router()

@router.message(CommandStart())
async def on_start(msg: Message):
    await msg.answer(
        "<b>Привет!</b> Я бот про ЗОЖ, питание и тренировки.\n\n"
        "Открой меню снизу или введи /help.",
        reply_markup=main_menu_kb()
    )

@router.message(Command("help"))
async def on_help(msg: Message):
    text = (
        "<b>Что я умею</b>\n"
        "• Анкета профиля и расчёт норм калорий/БЖУ\n"
        "• План тренировок на неделю и «Сегодня»\n"
        "• История + стрик\n"
        "• Напоминания: вода и время тренировки\n\n"

        "<b>Команды</b>\n"
        " /start — главное меню\n"
        " /profile — анкета пользователя\n"
        " /norms — мои нормы (ккал/БЖУ)\n"
        " /menu — пример меню на день\n"
        " /workout — тренировки (кнопки)\n"
        " /gym — план зала (неделя)\n"
        " /history — история тренировок\n"
        " /streak — серия подряд\n"
        " /undo — отменить отметку за сегодня\n"
        " /reminders — статус напоминаний\n"
        " /water_on /water_off — вода вкл/выкл\n"
        " /setworkout 19:00 — время тренировки\n"
        " /unsetworkout — убрать напоминание\n"
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="🏋️ Тренировки", callback_data="menu:workouts")
    kb.button(text="📝 Анкета", callback_data="menu:profile")
    kb.button(text="📊 Нормы", callback_data="help:norms_hint")
    kb.button(text="⏰ Напоминания", callback_data="menu:reminders")
    kb.adjust(2)

    await msg.answer(text, reply_markup=kb.as_markup())

# Подсказка по нормам из кнопки «📊 Нормы»
@router.callback_query(F.data == "help:norms_hint")
async def help_norms(cb: CallbackQuery):
    await cb.message.answer("Чтобы посчитать нормы, сначала пройди /profile, затем введи /norms.")
    await cb.answer()

# Кнопка «⏰ Напоминания» в /help
@router.callback_query(F.data == "menu:reminders")
async def go_reminders(cb: CallbackQuery):
    await cb.message.answer(
        "Напоминания:\n"
        "• /water_on — вода каждые 2 часа (10–20)\n"
        "• /water_off — отключить\n"
        "• /setworkout 19:00 — время тренировки ежедневно\n"
        "• /unsetworkout — убрать время\n"
        "• /reminders — посмотреть статус"
    )
    await cb.answer()
