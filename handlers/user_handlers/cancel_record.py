import time
from datetime import datetime

from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session

from api.cancel_record import delete_record
from handlers.user_handlers.schedulers import remove_jobs
from keyboards.keyboards_utils import create_inline_kb
from lexicon.buttons import accept_cancel
from states.states import GetEditRecordFSM
from utils.utils_db import get_user_token_of_client

current_year = datetime.now().year


router = Router()


@router.callback_query(StateFilter(GetEditRecordFSM.cancel_record))
async def send_accept_for_cancel(callback: types.CallbackQuery,
                                 state: FSMContext) -> None:
    """Хэндлер реагирует на состояние GetEditRecordFSM.cancel_record и
    отправляет вопрос об уверенности отмены записи."""

    await callback.message.edit_text('Загрузка... ⏳')
    adjust = (2, 2)
    inline_keyboard = create_inline_kb(adjust, **accept_cancel)
    time.sleep(0.5)
    await callback.message.edit_text(
        text='Вы уверены что хотите отменить запись?',
        reply_markup=inline_keyboard
    )
    await state.set_state(GetEditRecordFSM.cancel_record_accepting)


@router.callback_query(StateFilter(GetEditRecordFSM.cancel_record_accepting))
async def cancel_record(callback: types.CallbackQuery, session: Session,
                        state: FSMContext,
                        scheduler: AsyncIOScheduler) -> None:
    """Хэндлер реагирует на состояние GetEditRecordFSM.cancel_record_accepting
    и, в зависимости от callback, отменяет или не отменяет запись."""

    if callback.data == 'accept':
        await callback.message.edit_text('Отменяю запись... ⏳')
        state_data = await state.get_data()
        record_id = state_data['record_id']
        telegram_id = callback.from_user.id
        user_token = get_user_token_of_client(session, telegram_id)
        delete_record(record_id, user_token)

        user_id = callback.from_user.id
        remove_jobs(scheduler, user_id)

        time.sleep(0.5)
        await callback.message.edit_text(
            text='Запись успешно отменена! ✅'
        )
        await state.clear()

    elif callback.data == 'cancel':
        await callback.message.edit_text('Загрузка... ⏳')
        time.sleep(0.5)
        await callback.message.edit_text(
            text=('Запись не отменена!'))
        await state.clear()
