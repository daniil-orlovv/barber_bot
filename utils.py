import datetime

from aiogram.fsm.context import FSMContext

from api import get_free_date, get_free_time
from models import DataForRecord


async def check_date_for_staff(date_str: str, state: FSMContext) -> bool:
    state_data = await state.get_data()
    staff_id = state_data['staff']

    month, day = date_str.split('-')
    free_days = get_free_date(staff_id)  # Получаем доступные дни

    if month in free_days and day in free_days[month]:
        return True
    return False


async def check_free_services_for_staff(callback, state, api):

    state_data = await state.get_data()
    staffs = state_data['staff']
    free_staffs = api(staffs)
    return callback.data in free_staffs


async def check_free_time_for_staff(callback, state):

    state_data = await state.get_data()
    date = state_data['date']
    staff_id = state_data['staff']

    return callback.data in get_free_time(date, staff_id)


def return_month(value):
    months_key = {
        '1': 'Января', '2': 'Февраля', '3': 'Марта', '4': 'Апреля', '5': 'Мая',
        '6': 'Июня', '7': 'Июля', '8': 'Августа', '9': 'Сентября',
        '10': 'Октября', '11': 'Ноября', '12': 'Декабря'
    }
    return months_key.get(value)


def create_object_for_db(kwargs):

    time = kwargs['time']
    month_day = kwargs['date']
    current_year = datetime.datetime.now().year
    date_for_api = f'{current_year}-{month_day}T{time}:00.000Z'

    object_db = DataForRecord(
        staff=kwargs['staff'],
        service=kwargs['service'],
        date=kwargs['date'],
        time=kwargs['time'],
        name=kwargs['name'],
        phone=kwargs['phone'],
        email=kwargs['email'],
        comment=kwargs['comment']
    )
    return object_db
