# states.py
from aiogram.fsm.state import State, StatesGroup

class BookingStates(StatesGroup):
    name = State()
    phone = State()
    program = State()
    people_count = State()
    date = State()