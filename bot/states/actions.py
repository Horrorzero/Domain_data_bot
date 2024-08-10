from aiogram.fsm.state import StatesGroup, State


class Actions(StatesGroup):
    waiting_for_action = State()
    waiting_for_domains_to_delete = State()
