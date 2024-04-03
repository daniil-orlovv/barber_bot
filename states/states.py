from aiogram.fsm.state import State, StatesGroup


class SignUpFSM(StatesGroup):
    staff = State()
    service = State()
    date = State()
    time = State()
    check_data = State()
    name = State()
    phone = State()
    email = State()
    comment = State()
    accept_session = State()
