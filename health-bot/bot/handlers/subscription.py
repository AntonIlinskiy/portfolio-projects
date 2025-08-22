from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

router = Router()

SUB_TEXT = (
    "💳 <b>Подписка Premium</b>\n\n"
    "Что даёт:\n"
    "• Индивидуальные планы питания\n"
    "• Персональные тренировки\n"
    "• Напоминания и расширенная статистика\n\n"
    "Стоимость: <b>299 руб/мес</b>\n"
    "Для активации — напиши администратору."
)

@router.message(Command("premium"))
async def premium_cmd(msg: Message):
    await msg.answer(SUB_TEXT)

# Inline-кнопка «💳 Подписка»
@router.callback_query(F.data == "menu:billing")
async def premium_cb(cb: CallbackQuery):
    await cb.message.answer(SUB_TEXT)
    await cb.answer()

@router.message(F.text == "💳 Подписка")
async def premium_txt(msg: Message):
    await msg.answer(SUB_TEXT)
