from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from datetime import datetime
import json
from pathlib import Path

from bot.keyboards import main_menu

router = Router()

PROMO_FILE = Path(__file__).parent.parent / "data" / "promotions.json"

def load_promo():
    try:
        with open(PROMO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        title = data.get("title")
        description = data.get("description")
        valid_until = data.get("valid_until")
        if not (title and description and valid_until):
            return None
        until = datetime.strptime(valid_until, "%Y-%m-%d").date()
        if datetime.now().date() > until:
            return None
        return {
            "title": title,
            "description": description,
            "valid_until": until.strftime("%d.%m.%Y")
        }
    except Exception:
        return None

@router.message(StateFilter(None), F.text == "🔥 Акции и скидки")
async def show_promotions(message: Message):
    promo = load_promo()
    if not promo:
        await message.answer(
            "На данный момент активных акций нет.\n"
            "Загляните позже — у нас регулярно появляются выгодные предложения!",
            reply_markup=main_menu()
        )
        return
    text = (
        f"🔥 <b>{promo['title']}</b>\n\n"
        f"{promo['description']}\n\n"
        f"⏳ Действует до: <b>{promo['valid_until']}</b>"
    )
    await message.answer(text, reply_markup=main_menu(), parse_mode="HTML")
