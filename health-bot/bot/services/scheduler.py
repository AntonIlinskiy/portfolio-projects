# bot/services/scheduler.py
from typing import Iterable
from apscheduler.schedulers.asyncio import AsyncIOScheduler # type: ignore
from apscheduler.jobstores.base import ConflictingIdError # type: ignore
from aiogram import Bot

# ЕДИНСТВЕННЫЙ экземпляр планировщика (singleton)
scheduler = AsyncIOScheduler()

def _job_id(tg_id: int, kind: str) -> str:
    return f"{tg_id}:{kind}"

async def _notify(bot: Bot, tg_id: int, text: str):
    try:
        await bot.send_message(tg_id, text)
    except Exception:
        # не даём джобам падать из-за ошибок отправки
        pass

def schedule_user_reminders(bot: Bot, tg_id: int, reminders: Iterable):
    """
    Создаёт/обновляет расписание напоминаний для пользователя.
    Поддерживаются kind: 'water' (каждые 2 часа 10–20) и 'workout' (ежедневно HH:MM).
    """
    # Сносим старые задачи пользователя (и возможные water_* пресеты)
    for job in list(scheduler.get_jobs()):
        if job.id.startswith(f"{tg_id}:"):
            job.remove()

    for r in reminders:
        if r.kind == "water" and r.enabled:
            for h in [10, 12, 14, 16, 18, 20]:
                jid = _job_id(tg_id, f"water_{h}")
                try:
                    scheduler.add_job(
                        _notify, "cron",
                        args=[bot, tg_id, "💧 Время воды: сделай несколько глотков!"],
                        hour=h, minute=0,
                        id=jid, replace_existing=True,
                    )
                except ConflictingIdError:
                    pass

        elif r.kind == "workout" and r.enabled and r.time_str:
            hh, mm = map(int, r.time_str.split(":"))
            jid = _job_id(tg_id, "workout")
            try:
                scheduler.add_job(
                    _notify, "cron",
                    args=[bot, tg_id, "⏰ Тренировка! Открой /workout → «Сегодня» 💪"],
                    hour=hh, minute=mm,
                    id=jid, replace_existing=True,
                )
            except ConflictingIdError:
                pass
