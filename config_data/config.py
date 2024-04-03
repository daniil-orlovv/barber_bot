from typing import Union

from dataclasses import dataclass
from environs import Env
from aiogram import types

location = types.Location(latitude=59.869865, longitude=30.319785)

TIME = 'Время работы:  10:00 - 22:00'
PHONE = 'Телефон:  +7 921 565-16-15'
ADDRESS = 'Адрес:  Московский пр-т., 159'
BASE_URL = 'https://api.yclients.com/api/v1'


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
