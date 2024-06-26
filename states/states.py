from aiogram.fsm.state import State, StatesGroup


class SignUpFSM(StatesGroup):
    staff = State()
    service = State()
    date = State()
    time = State()
    check_data = State()
    name = State()
    phone = State()
    check_data = State()
    check_record = State()
    accept_session = State()


class GetEditRecordFSM(StatesGroup):
    choise_records = State()
    choise_actions = State()
    edit_record_date = State()
    edit_record_time = State()
    edit_accepting = State()
    cancel_record = State()
    cancel_record_accepting = State()


class FeedbackMaster(StatesGroup):
    waiting_text = State()
    waiting_mark = State()
    waiting_name = State()
    waiting_accepting = State()


class FeedbackCompany(StatesGroup):
    waiting_text = State()
    waiting_mark = State()
    waiting_name = State()
    waiting_accepting = State()


class Auth(StatesGroup):
    waiting_phone = State()
    waiting_name = State()
    waiting_code = State()
