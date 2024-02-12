from api import get_free_date


def check_date(date_str: str) -> bool:
    month, day = date_str.split('-')
    free_days = get_free_date()  # Получаем доступные дни

    if month in free_days and day in free_days[month]:
        return True
    return False


def return_month(value):
    months_key = {
        '1': 'Января', '2': 'Февраля', '3': 'Марта', '4': 'Апреля', '5': 'Мая',
        '6': 'Июня', '7': 'Июля', '8': 'Августа', '9': 'Сентября',
        '10': 'Октября', '11': 'Ноября', '12': 'Декабря'
    }
    return months_key.get(value)
