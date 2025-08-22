from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from .models import User, WorkoutLog, Reminder
from datetime import datetime, timedelta


def get_user_by_tg(db: Session, tg_id: int) -> User | None:
    return db.execute(select(User).where(User.tg_id == tg_id)).scalar_one_or_none()

def get_or_create_user(db: Session, tg_id: int) -> User:
    u = get_user_by_tg(db, tg_id)
    if u:
        return u
    
    u = User(tg_id=tg_id)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def update_user(db: Session, user: User, **fields) -> User:
    for k, v in fields.items():
        setattr(user, k, v)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user    

def add_workout_log(db: Session, tg_id: int, day: int | None, title: str | None) -> WorkoutLog:
    log = WorkoutLog(tg_id=tg_id, day=day, title=title)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_recent_logs(db: Session, tg_id: int, limit: int = 10) -> list[WorkoutLog]:
    q = db.query(WorkoutLog).filter(WorkoutLog.tg_id == tg_id).order_by(WorkoutLog.performed_at.desc()).limit(limit)
    return q.all()

def get_streak_days(db: Session, tg_id: int) -> int:
    """Подсчитать текущий стрик (подряд по дням). Считаем: сегодня/вчера/позавчера и т.д., если в день есть хотя бы один лог."""
    logs = db.query(WorkoutLog).filter(WorkoutLog.tg_id == tg_id).order_by(WorkoutLog.performed_at.desc()).limit(60).all()
    if not logs:
        return 0
    days = {log.performed_at.date() for log in logs if hasattr(log.performed_at, "date")}
    if not days:
        return 0
    streak = 0
    today = datetime.now().date()
    d = today
    while d in days:
        streak += 1
        d = d - timedelta(days=1)
    return streak

def undo_today_log(db: Session, tg_id: int) -> bool:
    today = datetime.now().date()
    q = (
        db.query(WorkoutLog)
        .filter(WorkoutLog.tg_id == tg_id)
        .order_by(desc(WorkoutLog.performed_at))
    )
    for row in q:
        if hasattr(row.performed_at, "date") and row.performed_at.date() == today:
            db.delete(row)
            db.commit()
            return True
        return False
    
def get_reminders_for_user(db: Session, tg_id: int) -> list[Reminder]:
    return db.query(Reminder).filter(Reminder.tg_id == tg_id).all()

def upsert_workout_reminder(db: Session, tg_id: int, time_str: str | None) -> Reminder:
    r = db.query(Reminder).filter(Reminder.tg_id==tg_id, Reminder.kind=='workout').one_or_none()
    if r is None:
        r = Reminder(tg_id=tg_id, kind="workout", time_str=time_str, enabled=bool(time_str))
    else:
        r.time_str = time_str
        r.enabled = bool(time_str)
    db.add(r); db.commit(); db.refresh(r)
    return r

def set_water_reminder(db: Session, tg_id: int, enabled: bool) -> Reminder:
   r = db.query(Reminder).filter(Reminder.tg_id==tg_id, Reminder.kind=='water').one_or_none()
   if r is None:
       r = Reminder(tg_id=tg_id, kind="water", time_str=None, enabled=enabled)
   else:
       r.enabled = enabled
   db.add(r); db.commit(); db.refresh(r)
   return r
   
   
   
         

