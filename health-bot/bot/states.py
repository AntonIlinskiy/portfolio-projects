# bot/states.py
from aiogram.fsm.state import StatesGroup, State

class ProfileForm(StatesGroup):
    name = State()
    sex = State()
    age = State()
    height = State()
    weight = State()
    goal = State()
    activity = State()
    diet = State()
    allergies = State()
    confirm = State()
