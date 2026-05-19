"""FSM holatlari."""
from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    language = State()
    name = State()
    phone = State()


class Settings(StatesGroup):
    menu = State()
    waiting_language = State()
    waiting_name = State()
    waiting_phone = State()


class AdminAnswer(StatesGroup):
    waiting_answer = State()
