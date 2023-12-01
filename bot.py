from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = '6691199047:AAHOr-ueqvD9Qn7WsVEx_YspHknm_6i5UXU'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ бот Максуда!\nДавай запишу тебя на стрижку!')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


@dp.message(Command(commands=['about']))
async def process_about_command(message: Message):
    await message.answer(
        'Адрес:  Московский пр-т., 159\n'
        'Время работы:  10:00-22:00\n'
        'Телефон:  +7 921 565-16-15\n'
    )


if __name__ == '__main__':
    dp.run_polling(bot)
