from aiogram import F, Router
from aiogram.types import Message

from api.get_services import get_all_services

router = Router()


@router.message(F.text == 'Все услуги ✂️')
async def services(message: Message) -> None:
    """Хэндлер реагирует на кнопку с надписью 'Все услуги ✂️' и оптравляет все
    доступные услуги компании."""

    info_services = get_all_services()

    msg = ''
    for title, cost in info_services.items():
        msg += f"✂️{title} -  💵{cost} руб.\n"
    await message.answer(text=msg)
