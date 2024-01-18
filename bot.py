from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram import types

from config import BOT_TOKEN, location, TIME, PHONE, ADDRESS
from keyboards import (button_contacts, button_sign_up, url_button,
                       create_inline_kb, create_keyboards,
                       digital_of_month, times)
from requests_of_api import get_free_date


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
    first_month = free_days.get('1')
    keyboard = create_inline_kb(7, *first_month)
    await message.answer(
        text='Свободные даты на текущий месяц:',
        reply_markup=keyboard
    )


@dp.callback_query(lambda callback: callback.data in digital_of_month)
async def send_times(callback: types.CallbackQuery):
    keyboard_times = create_inline_kb(3, *times)
    keyboard = create_keyboards(1, 'Отменить запись')
    await callback.message.answer(
        text="Выберите доступное время:",
        reply_markup=keyboard_times
    )
    await callback.message.answer(
        text='Вы можете отменить запись:',
        reply_markup=keyboard
    )


@dp.callback_query(lambda callback: callback.data in times)
async def send_answer_order(callback: types.CallbackQuery):
    await callback.message.answer(
        text="Отлично, вы записаны!",
        reply_markup=keyboard
    )


@dp.message(F.text == 'Выбрать услугу')
async def command_services(message: Message):
    keyboard = create_inline_kb(3, 'Услуга 1', 'Услуга 2', 'Услуга 3')
    await message.answer(
        text='Услуги:',
        reply_markup=keyboard
    )


@dp.message(F.text == 'Отменить запись')
async def command_cancel(message: Message):
    await message.answer(
        text='Выбери дейстие:',
        reply_markup=keyboard
    )


if __name__ == '__main__':
    dp.run_polling(bot)
