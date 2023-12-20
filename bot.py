from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup

from config import BOT_TOKEN, location
from keyboards import button_contacts, button_map


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
keyboard = ReplyKeyboardMarkup(keyboard=[[button_contacts, button_map]],
                               resize_keyboard=True)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        text='Привет!\nЯ бот Максуда!'
             '\nДавай запишу тебя на стрижку!',
        reply_markup=keyboard
    )


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение'
    )


@dp.message(F.text == 'Контакты')
async def command_contacts(message: Message):
    await message.answer(
        text='Телефон:  +7 921 565-16-15'
    )


@dp.message(F.text == 'Мы на карте')
async def command_map(message: Message):
    await message.answer_location(
        location.latitude,
        location.longitude
    )
    await message.answer('Московский пр-т., 159')


if __name__ == '__main__':
    dp.run_polling(bot)
