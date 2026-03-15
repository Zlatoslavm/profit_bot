from aiogram.dispatcher.filters.state import State, StatesGroup

class ProfitForm(StatesGroup):
    user = State()
    amount = State()
    device = State()
    status = State()

class AdminForm(StatesGroup):
    add_id = State()
    add_name = State()
    del_id = State()

class LockState(StatesGroup):
    device = State()
    worker = State()
    locker = State()