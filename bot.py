from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup

from config import BOT_TOKEN, location, TIME, PHONE, ADDRESS
from keyboards import button_contacts, button_sign_up, url_button


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
async def command_sign_up(message: Message):
    await message.answer(
        text='Нажмите на кнопку:',
        reply_markup=sigh_up_keyboard
        )


if __name__ == '__main__':
    dp.run_polling(bot)
