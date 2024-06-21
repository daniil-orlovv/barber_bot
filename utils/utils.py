from datetime import datetime

current_year = datetime.now().year


def return_month(value):
    months_key = {
        '1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель', '5': 'Май',
        '6': 'Июнь', '7': 'Июль', '8': 'Август', '9': 'Сентябрь',
        '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'
    }
    return months_key.get(value)


def to_normalize_date(date):

    invert_date = date.split('-')[::-1]
    normal_date = (
        f'{invert_date[0]} {return_month(invert_date[1])} {current_year}')
    return normal_date


def return_date_iso8601(year, month, day, time):
    return f'{year}-{int(month):02}-{int(day):02}T{time}:00+0300'


def return_date_for_records(date):
    parts = date.split()

    date = parts[0]
    time = parts[1]
    time = time[:5]

    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y")

    new_string = f"{formatted_date} {time}"
    return new_string
