from __future__ import annotations
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path(__file__).resolve().parent.parent / "bot" / "data" / "booking.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def _connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON;")
    return con

def init_db(reset: bool = False) -> None:
    """
    Создать (или пересоздать) таблицы.
    """
    with _connect() as con:
        cur = con.cursor()
        if reset:
            cur.execute("DROP TABLE IF EXISTS slots;")
            cur.execute("DROP TABLE IF EXISTS bookings;")
       
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slot_date TEXT NOT NULL,       -- YYYY-MM-DD
                slot_time TEXT NOT NULL,       -- HH:MM
                taken INTEGER NOT NULL DEFAULT 0,
                user_id INTEGER,
                service TEXT,
                brand TEXT,
                model TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                UNIQUE(slot_date, slot_time)
            );
            """
        )
        
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                service TEXT,
                brand TEXT,
                model TEXT,
                slot_date TEXT NOT NULL,
                slot_time TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            """
        )
        con.commit()

def seed_slots_for_date(date_str: str, times: list[str]) -> None:
    """
    Закинуть в таблицу слоты на конкретную дату (если их ещё нет).
    """
    with _connect() as con:
        cur = con.cursor()
        for t in times:
            try:
                cur.execute(
                    "INSERT OR IGNORE INTO slots (slot_date, slot_time, taken) VALUES (?, ?, 0)",
                    (date_str, t),
                )
            except sqlite3.Error:
                pass
        con.commit()

def seed_default_week() -> None:
    """
    Засеять слоты на ближайшие 7 дней по шаблону времени.
    """
    times = ["10:00", "11:00", "12:00", "13:00", "15:00", "16:00", "17:00"]
    today = datetime.now().date()
    for i in range(7):
        d = today + timedelta(days=i)
        seed_slots_for_date(d.isoformat(), times)

def list_free_slots(date_str: str, limit: int | None = None) -> list[str]:
    """
    Вернуть свободные времена для указанной даты (taken = 0).
    """
    sql = "SELECT slot_time FROM slots WHERE slot_date = ? AND taken = 0 ORDER BY slot_time"
    params = (date_str,)
    with _connect() as con:
        cur = con.execute(sql, params)
        rows = [r[0] for r in cur.fetchall()]
    return rows[:limit] if limit else rows

def reserve_slot(
    date_str: str,
    time_str: str,
    user_id: int,
    service: str | None,
    brand: str | None,
    model: str | None,
) -> bool:
    """
    Попытаться занять слот. Возвращает True если получилось.
    """
    with _connect() as con:
        cur = con.cursor()
        
        cur.execute(
            "SELECT id, taken FROM slots WHERE slot_date = ? AND slot_time = ?",
            (date_str, time_str),
        )
        row = cur.fetchone()
        if not row:
            return False
        slot_id, taken = row
        if taken:
            return False

        
        cur.execute(
            "UPDATE slots SET taken = 1, user_id = ?, service = ?, brand = ?, model = ? WHERE id = ?",
            (user_id, service, brand, model, slot_id),
        )
        
        cur.execute(
            """
            INSERT INTO bookings (user_id, service, brand, model, slot_date, slot_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, service, brand, model, date_str, time_str, datetime.now().isoformat(timespec="seconds")),
        )
        con.commit()
        return True

def get_user_bookings(user_id: int) -> list[tuple]:
    """
    История бронирований пользователя.
    """
    with _connect() as con:
        cur = con.execute(
            "SELECT slot_date, slot_time, service, brand, model, created_at FROM bookings WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
        return cur.fetchall()
