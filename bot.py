import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram import types
from dotenv import load_dotenv

from config import location, TIME, PHONE, ADDRESS
from keyboards import (button_contacts, button_sign_up, url_button,
                       create_keyboards, create_inline_kb,
                       times)
from api import get_free_date, get_free_time, get_free_services

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN', default='bot_token')

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
keyboard = ReplyKeyboardMarkup(keyboard=[[button_contacts, button_sign_up]],
                               resize_keyboard=True)

sigh_up_keyboard = InlineKeyboardMarkup(inline_keyboard=[[url_button]])


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        text='Привет!\nЯ бот Максуда!'
             '\nДавай запишу тебя на стрижку!',
        reply_markup=keyboard
    )


@dp.message(F.text == 'Контакты')
async def command_contacts(message: Message):
    await message.answer_location(
        location.latitude,
        location.longitude
    )
    await message.answer(f"{ADDRESS}\n{TIME}\n{PHONE}")


@dp.message(F.text == 'Записаться')
async def command_sign_up_test(message: Message):
    await message.answer(
        text='Нажмите на кнопку:',
        reply_markup=create_keyboards(
            2,
            "Выбрать дату и время",
            "Выбрать услугу",
            "Отменить запись")
        )


@dp.message(F.text == 'Выбрать дату и время')
async def command_sign_up_time(message: Message):
    free_days = get_free_date()
    count_months = len(free_days)
    adjust = (1, 7, 7, 7, 7, 7)
    for i in range(0, count_months):
        month = str(i + 1)
        days = free_days.get(month)
        params = (month, days)
        keyboard = create_inline_kb(adjust, 'date', *params)
        await message.answer(
            text='Ближайшие свободные даты:',
            reply_markup=keyboard
        )


@dp.callback_query(lambda callback: callback.data.startswith('1'))
async def send_times(callback: types.CallbackQuery):
    month, day = callback.data.split('_')
    date = f'2024-01-{day}'
    adjust = (1, 7, 7, 7, 7, 7)
    free_times = get_free_time(date)
    params = [date, free_times]
    keyboard_times = create_inline_kb(adjust, 'time', *params)
    keyboard_cancel = create_keyboards(1, 'Отменить запись')
    await callback.message.answer(
        text="Выберите доступное время:",
        reply_markup=keyboard_times
    )
    await callback.message.answer(
        text='Вы можете отменить запись:',
        reply_markup=keyboard_cancel
    )


@dp.callback_query(lambda callback: callback.data.startswith('time_'))
async def send_services(callback: types.CallbackQuery):
    time = callback.data.split('_')[1]
    adjust = (2, 2, 2)
    free_services = get_free_services()
    keyboard_times = create_inline_kb(adjust, 'service', *free_services)
    keyboard_cancel = create_keyboards(1, 'Отменить запись')
    await callback.message.answer(
        text="Выберите услугу:",
        reply_markup=keyboard_times
    )
    await callback.message.answer(
        text='Вы можете отменить запись:',
        reply_markup=keyboard_cancel
    )


@dp.callback_query(lambda callback: callback.data in times)
async def send_answer_order(callback: types.CallbackQuery):
    await callback.message.answer(
        text="Отлично, вы записаны!",
        reply_markup=keyboard
    )


@dp.message(F.text == 'Выбрать услугу')
async def command_services(message: Message):
    adjust = (2, 2, 2)
    free_services = get_free_services()
    keyboard_times = create_inline_kb(adjust, 'service', *free_services)
    keyboard_cancel = create_keyboards(1, 'Отменить запись')
    await message.answer(
        text="Выберите услугу:",
        reply_markup=keyboard_times
    )
    await message.answer(
        text='Вы можете отменить запись:',
        reply_markup=keyboard_cancel
    )


@dp.message(F.text == 'Отменить запись')
async def command_cancel(message: Message):
    await message.answer(
        text='Выбери дейстие:',
        reply_markup=keyboard
    )


if __name__ == '__main__':
    dp.run_polling(bot)
