import time
from datetime import datetime

from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.keyboards_utils import create_inline_kb, create_calendar
from api.create_record import get_free_date, get_free_time
from api.edit_record import edit_record
from api.get_records import get_record_by_id
from api.cancel_record import delete_record
from utils.utils import return_date_for_records
from utils.utils_db import get_user_token_of_client
from states.states import GetEditRecordFSM
from lexicon.buttons import edit_cancel, accept_cancel

current_year = datetime.now().year


router = Router()


@router.callback_query(StateFilter(GetEditRecordFSM.choise_records))
async def one_record(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text('Загружаю запись... ⏳')
    record_id = callback.data
    print(record_id)
    telegram_id = callback.from_user.id
    user_token = get_user_token_of_client(telegram_id)
    record = get_record_by_id(record_id, user_token)
    title = record.get('title')
    name_staff = record.get('name_staff')
    cost = record.get('cost')
    date = record.get('date')
    normal_date = return_date_for_records(date)

    staff_id = record.get('staff_id')
    service_id = record.get('service_id')
    client_id = record.get('client_id')
    seance_length = record.get('seance_length')

    await state.update_data(record_id=record_id, staff_id=staff_id,
                            service_id=service_id, client_id=client_id,
                            title=title, name_staff=name_staff, cost=cost,
                            seance_length=seance_length)

    adjust = (2, 2)
    inline_keyboard = create_inline_kb(adjust, **edit_cancel)
    time.sleep(0.5)
    await callback.message.edit_text(
        text=(f'Услуга: {title}\n'
              f'Мастер: {name_staff}\n'
              f'Стоимость: {cost} руб.\n'
              f'Дата: {normal_date}'),
        reply_markup=inline_keyboard)
    await state.set_state(GetEditRecordFSM.choise_actions)


@router.callback_query(StateFilter(GetEditRecordFSM.choise_actions))
async def edit_or_cancel(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'edit':
        await callback.message.edit_text('Ищу свободные даты... ⏳')
        state_data = await state.get_data()
        staff_id = state_data['staff_id']
        free_days = get_free_date(staff_id)
        inline_calendar = create_calendar(free_days)
        time.sleep(0.5)
        await callback.message.edit_text(
            text='Выберите дату:',
            reply_markup=inline_calendar
        )
        await state.set_state(GetEditRecordFSM.edit_record_date)

    elif callback.data == 'cancel':
        await callback.message.edit_text('Загрузка... ⏳')
        adjust = (2, 2)
        inline_keyboard = create_inline_kb(adjust, **accept_cancel)
        time.sleep(0.5)
        await callback.message.edit_text(
            text='Отменить запись?',
            reply_markup=inline_keyboard
        )
        await state.set_state(GetEditRecordFSM.cancel_record)


@router.callback_query(StateFilter(GetEditRecordFSM.edit_record_date))
async def send_time(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text('Ищу свободное время... ⏳')
    month, day = callback.data.split('-')
    date = f'{current_year}-{month}-{day}'
    state_data = await state.get_data()
    await state.update_data(new_date=date)
    staff_id = state_data['staff_id']
    print(date, staff_id)
    free_times = get_free_time(staff_id, date)
    adjust = (4, 4, 4, 4, 4, 4,)
    keyboard_times = create_inline_kb(adjust, *free_times)
    time.sleep(0.5)
    await callback.message.edit_text(
        text='Выберите время:',
        reply_markup=keyboard_times
    )
    await state.set_state(GetEditRecordFSM.edit_record_time)


@router.callback_query(StateFilter(GetEditRecordFSM.edit_record_time))
async def send_accept_for_edit(callback: types.CallbackQuery,
                               state: FSMContext):

    await callback.message.edit_text('Загрузка... ⏳')
    new_time = callback.data
    state_data = await state.get_data()
    await state.update_data(new_time=new_time)
    adjust = (2, 2)
    inline_keyboard = create_inline_kb(adjust, **accept_cancel)

    time.sleep(0.5)
    await callback.message.edit_text(
        text=(f'Услуга: {state_data["title"]}\n'
              f'Мастер: {state_data["name_staff"]}\n'
              f'Стоимость: {state_data["cost"]} руб.\n'
              f'Дата: {state_data["new_date"]}'
              f'Время: {new_time}\n\n'
              'Перенести запись на это время?'),
        reply_markup=inline_keyboard
    )

    await state.set_state(GetEditRecordFSM.edit_accepting)


@router.callback_query(StateFilter(GetEditRecordFSM.edit_accepting))
async def update_record(callback: types.CallbackQuery, state: FSMContext):

    if callback.data == 'accept':

        await callback.message.edit_text('Переношу запись... ⏳')
        state_data = await state.get_data()
        title = state_data['title']
        name_staff = state_data['name_staff']
        service_cost = state_data['cost']
        new_date = state_data['new_date']
        new_time = state_data['new_time']

        edit_record(state_data)

        time.sleep(0.5)
        await callback.message.edit_text(
            text=(f'Запись перенесена! ✅\n\n'
                  f'Услуга: {title}\n'
                  f'Мастер: {name_staff}\n'
                  f'Стоимость: {service_cost} руб.\n'
                  f'Дата: {new_date}\n'
                  f'Время: {new_time}')
        )
        await state.clear()

    elif callback.data == 'cancel':
        await callback.message.edit_text('Отменяю перенос... ⏳')
        time.sleep(0.5)
        await callback.message.edit_message(
            text=('Перенос записи отменен!'))
        await state.clear()


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
async def cancel_record(callback: types.CallbackQuery, state: FSMContext):

    if callback.data == 'accept':
        await callback.message.edit_text('Отменяю запись... ⏳')
        state_data = await state.get_data()
        record_id = state_data['record_id']
        telegram_id = callback.from_user.id
        user_token = get_user_token_of_client(telegram_id)
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
