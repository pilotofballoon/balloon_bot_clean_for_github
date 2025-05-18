# states.py

from aiogram.fsm.state import State, StatesGroup

class BookingStates(StatesGroup):
    name = State()
    contact = State()
    program = State()
    people_count = State()
    date = State()