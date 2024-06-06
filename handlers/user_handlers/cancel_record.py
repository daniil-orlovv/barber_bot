import time
from datetime import datetime

from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.keyboards_utils import create_inline_kb
from api.cancel_record import delete_record
from utils.utils_db import get_user_token_of_client
from states.states import GetEditRecordFSM
from lexicon.buttons import accept_cancel
from sqlalchemy.orm import Session

current_year = datetime.now().year


router = Router()


@router.callback_query(StateFilter(GetEditRecordFSM.cancel_record))
async def send_accept_for_cancel(callback: types.CallbackQuery,
                                 state: FSMContext):

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
                        state: FSMContext):

    if callback.data == 'accept':
        await callback.message.edit_text('Отменяю запись... ⏳')
        state_data = await state.get_data()
        record_id = state_data['record_id']
        telegram_id = callback.from_user.id
        user_token = get_user_token_of_client(session, telegram_id)
        delete_record(record_id, user_token)
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
