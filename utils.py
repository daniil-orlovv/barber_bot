from aiogram.fsm.context import FSMContext

from api import get_free_date, get_free_time


def check_date(date_str: str) -> bool:
    month, day = date_str.split('-')
    free_days = get_free_date()  # Получаем доступные дни

    if month in free_days and day in free_days[month]:
        return True
    return False
