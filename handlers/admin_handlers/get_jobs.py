import datetime
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = logging.getLogger(__name__)

router = Router()


current_year = datetime.datetime.now().year


@router.message(Command(commands='jobs'))
async def get_jobs(message: Message, scheduler):

    jobs = scheduler.get_jobs()
    jobs_str = '\n'.join(map(str, jobs))
    await message.answer(text=jobs_str)


@router.message(Command(commands='remove'))
async def remove_jobs(message: Message, scheduler):
    cmd, id_job = message.text.split()
    scheduler.remove_job(id_job)
