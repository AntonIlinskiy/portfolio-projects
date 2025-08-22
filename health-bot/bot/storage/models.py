from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy import DateTime, func, String, Boolean, Integer, Float

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)

    name: Mapped[str | None] = mapped_column(String(64))
    sex : Mapped[str | None] = mapped_column(String(10))
    age : Mapped[int | None] = mapped_column(Integer)
    height: Mapped[float | None] = mapped_column(Float)
    weight: Mapped[float | None] = mapped_column(Float)
    goal: Mapped[str | None] = mapped_column(String(16))
    activity: Mapped[str | None] = mapped_column(String(16))
    diet: Mapped[str | None] = mapped_column(String(16))
    allergies: Mapped[str | None] = mapped_column(String(255))

    kcal: Mapped[int | None] = mapped_column(Integer)
    protein_g: Mapped[int | None] = mapped_column(Integer)
    fat_g: Mapped[int | None] = mapped_column(Integer)
    carbs_g: Mapped[int | None] = mapped_column(Integer)

    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)

class WorkoutLog(Base):
    __tablename__ = "workout_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int | None] = mapped_column(Integer, index=True)
    day: Mapped[int | None] = mapped_column(Integer)
    title: Mapped[str | None] = mapped_column(String(80))
    performed_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())    

class Reminder(Base):
    __tablename__ = "reminders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, index=True)
    kind: Mapped[str] = mapped_column(String(32))
    time_str: Mapped[str | None] = mapped_column(String(5))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)   

    