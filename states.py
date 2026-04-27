from aiogram.fsm.state import State, StatesGroup

class FinanceStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_desc = State()