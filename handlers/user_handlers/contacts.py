from aiogram import F, Router
from aiogram.types import Message

from config_data.config import location
from keyboards.keyboards_utils import create_inline_kb
import lexicon.lexicon_ru as lexicon
from lexicon.buttons import contacts_buttons

router = Router()


@router.message(F.text == 'Контакты 📍')
async def contacts(message: Message):

    inline_keyboard = create_inline_kb(contacts_buttons['adjust'],
                                       **contacts_buttons['buttons'])

    await message.answer_location(location.latitude, location.longitude)
    await message.answer(text=lexicon.ABOUT, reply_markup=inline_keyboard)
