from aiogram import F, Router
from aiogram.types import Message

from external_services.other_api import get_all_services

router = Router()


@router.message(F.text == 'Все услуги ✂️')
async def services(message: Message):

    info_services = get_all_services()

    mess = ''
    for title, cost in info_services.items():
        mess += f"✂️{title} -  💵{cost} руб.\n"
    await message.answer(text=mess)
