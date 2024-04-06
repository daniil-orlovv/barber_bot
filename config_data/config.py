import os
from typing import Union

from dataclasses import dataclass
from environs import Env
from aiogram import types
from dotenv import load_dotenv

load_dotenv()
PARTNER_TOKEN = os.getenv('PARTNER_TOKEN', default='partner_key')
USER_TOKEN = os.getenv('USER_TOKEN', default='user_token')
COMPANY_ID = os.getenv('COMPANY_ID', default='company_id')


location = types.Location(latitude=59.869865, longitude=30.319785)

TIME = 'Время работы:  10:00 - 22:00'
PHONE = 'Телефон:  +7 921 565-16-15'
ADDRESS = 'Адрес:  Московский пр-т., 159'
BASE_URL = 'https://api.yclients.com/api/v1'
ADRESS_URL_GOOGLE = 'https://www.google.ru/maps/place/Z+BARBERSHOP/@59.8701493,30.3182728,17.75z/data=!4m15!1m8!3m7!1s0x46963aa721dd1d6d:0xba23198df4c2848f!2z0JzQvtGB0LrQvtCy0YHQutC40Lkg0L_RgC3Rgi4sIDE1OSwg0KHQsNC90LrRgi3Qn9C10YLQtdGA0LHRg9GA0LMsIDE5NjEyOA!3b1!8m2!3d59.8701499!4d30.3198169!16s%2Fg%2F11c22kwr4p!3m5!1s0x46963b1c60044369:0x3c8c0fe07b9e8c44!8m2!3d59.869837!4d30.319718!16s%2Fg%2F11frsrrm0c?hl=ru&entry=ttu'
ADRESS_URL_YANDEX = 'https://yandex.ru/maps/2/saint-petersburg/?ll=30.319899%2C59.869541&mode=poi&poi%5Bpoint%5D=30.319922%2C59.869556&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D58764822381&z=20'
ADRESS_URL_2GIS = 'https://2gis.ru/spb/firm/70000001041414988/30.319888%2C59.869537?m=30.320061%2C59.869467%2F20'


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: Union[str, None] = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        )
    )
