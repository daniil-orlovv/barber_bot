from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session
from keyboards.keyboards_utils import create_inline_kb
from api.get_records import (get_title_and_date_of_records,
                             selection_of_records_by_company)
from states.states import GetEditRecordFSM

current_year = datetime.now().year


router = Router()


@router.message(F.text == 'Мои записи 📖')
async def all_records(message: Message, session: Session, state: FSMContext):

    telegram_id = message.from_user.id
    records_of_clients = selection_of_records_by_company(session, telegram_id)
    records = get_title_and_date_of_records(records_of_clients)
    if records:
        adjust = (1, 1, 1, 1, 1)
        inline_keyboard = create_inline_kb(adjust, **records)
        await message.answer(
            text='Для просмотра, переноса или отмены - выберите запись:',
            reply_markup=inline_keyboard
        )
        await state.set_state(GetEditRecordFSM.choise_records)
    else:
        await message.answer(
            text='Записи отсутствуют.'
        )
        await state.clear()
