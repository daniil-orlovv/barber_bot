import datetime

from models.models import DataForRecord


current_year = datetime.datetime.now().year


def return_month(value):
    months_key = {
        '1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель', '5': 'Май',
        '6': 'Июнь', '7': 'Июль', '8': 'Август', '9': 'Сентябрь',
        '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'
    }
    return months_key.get(value)


def create_registration_for_db(kwargs):

    object_db = DataForRecord(
        staff=kwargs['staff_name'],
        service=kwargs['service_title'],
        date=kwargs['date'],
        time=kwargs['time'],
        name=kwargs['name'],
        phone=kwargs['phone'],
        email=kwargs['email'],
        comment=kwargs['comment']
    )
    return object_db


def to_normalize_date(date):

    invert_date = date.split('-')[::-1]
    normal_date = (
        f'{invert_date[0]} {return_month(invert_date[1])} {current_year}')
    return normal_date


def return_date_iso8601(year, month, day, time):
    return f'{year}-{int(month):02}-{int(day):02}T{time}:00+0300'
