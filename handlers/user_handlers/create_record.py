import datetime
import logging

from aiogram import Bot, F, types, Router
from aiogram.types import Message
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from keyboards.keyboards_utils import (create_inline_kb, create_calendar,
                                       create_kb)
from external_services.create_api import (get_free_date, get_free_time,
                                          get_free_services, get_free_staff,
                                          create_session_api)
from external_services.edit_api import get_ycl_id
from utils.utils import create_registration_for_db, to_normalize_date
from utils.utils_db import add_client_in_db, add_record_in_db
from filters.filters import (CheckFreeStaff, CheckFreeService, CheckFreeDate,
                             CheckFreeTime, CheckCallbackAccept,
                             CheckCallbackCancel)
from states.states import SignUpFSM
import lexicon.lexicon_ru as lexicon
from lexicon.buttons import accept_cancel, start_buttons

logger = logging.getLogger(__name__)

router = Router()


current_year = datetime.datetime.now().year


@router.message(CommandStart())
async def start(message: Message):

    keyboard = create_kb(start_buttons['adjust'], *start_buttons['buttons'])
    await message.answer(text=lexicon.WELCOME_TEXT, reply_markup=keyboard)
    logger.debug('Send message from handler start')


@router.message(F.text == 'Записаться')
async def send_masters(message: Message, state: FSMContext):

    free_staffs = get_free_staff()
    inverted_staffs = {v: k for k, v in free_staffs.items()}

    adjust = (2, 2, 2)
    keyboard_inline = create_inline_kb(adjust, **free_staffs)

    await message.delete()
    await message.answer(text=lexicon.REG_MASTER, reply_markup=keyboard_inline)

    await state.update_data(all_staffs=inverted_staffs)
    await state.set_state(SignUpFSM.staff)

    logger.debug('Send message from handler contacts')
    logger.debug('Change State to staff')


@router.callback_query(CheckFreeStaff(), StateFilter(SignUpFSM.staff))
async def send_service(callback: types.CallbackQuery, state: FSMContext):

    staff_id = callback.data
    state_data = await state.get_data()
    all_staffs = state_data.get('all_staffs', {})
    staff_name = all_staffs.get(staff_id)
    await state.update_data(staff_name=staff_name, staff_id=staff_id)

    free_services = get_free_services(staff_id)
    inverted_services = {v: k for k, v in free_services.items()}
    await state.update_data(all_services=inverted_services)

    adjust = (2, 2, 2)
    keyboard_services = create_inline_kb(adjust, **free_services)

    await callback.message.edit_text(
        text=lexicon.REG_SERVICE.format(staff_name),
        reply_markup=keyboard_services
    )
    await state.set_state(SignUpFSM.service)
    logger.debug('Send message from handler send_service')
    logger.debug('Change State to service')


@router.callback_query(StateFilter(SignUpFSM.service), CheckFreeService())
async def send_date(callback: types.CallbackQuery, state: FSMContext):

    service_id = callback.data
    state_data = await state.get_data()
    staff_id = state_data['staff_id']
    staff_name = state_data['staff_name']

    all_services = state_data.get('all_services', {})
    service_title = all_services.get(service_id)
    await state.update_data(service_title=service_title)

    free_days = get_free_date(staff_id)
    keyboard = create_calendar(free_days)

    await callback.message.edit_text(
        text=lexicon.REG_DATE.format(staff_name, service_title),
        reply_markup=keyboard
    )
    await state.set_state(SignUpFSM.date)
    logger.debug('Send message from handler send_date')
    logger.debug('Change State to date')


@router.callback_query(StateFilter(SignUpFSM.date), CheckFreeDate())
async def send_time(callback: types.CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    staff_name = state_data['staff_name']
    staff_id = state_data['staff_id']
    service_title = state_data['service_title']

    month, day = callback.data.split('-')
    date = f'{current_year}-{month}-{day}'
    await state.update_data(date=date)
    norm_date = to_normalize_date(callback.data)
    adjust = (4, 4, 4, 4, 4, 4,)
    free_times = get_free_time(staff_id, date)
    keyboard_times = create_inline_kb(adjust, *free_times)

    await callback.message.edit_text(
        text=lexicon.REG_TIME.format(staff_name, service_title, norm_date),
        reply_markup=keyboard_times
    )
    await state.set_state(SignUpFSM.time)
    logger.debug('Send message from handler send_time')
    logger.debug('Change State to time')


@router.callback_query(StateFilter(SignUpFSM.time), CheckFreeTime())
async def pre_check(
    callback: types.CallbackQuery,
    state: FSMContext
):

    await state.update_data(time=callback.data)
    state_data = await state.get_data()
    staff_name = state_data['staff_name']
    service_title = state_data['service_title']
    date = state_data['date']
    date = to_normalize_date(date)
    time = state_data['time']

    adjust = (2, 1)
    keyboard = create_inline_kb(adjust, **accept_cancel)

    await callback.message.edit_text(
        text=lexicon.REG_CHECK.format(staff_name, service_title, date, time),
        reply_markup=keyboard
    )
    await state.set_state(SignUpFSM.check_data)
    logger.debug('Send message from handler pre_check')
    logger.debug('Change State to check_data')


@router.callback_query(StateFilter(SignUpFSM.check_data),
                       CheckCallbackCancel())
async def cancel(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text='Вы отменили процесс записи.'
    )
    await state.clear()
    logger.debug('Send message from handler cancel')
    logger.debug('Change State to default_state')


@router.callback_query(StateFilter(SignUpFSM.check_data),
                       CheckCallbackAccept())
async def get_name(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text=lexicon.REG_NAME)
    id_message = callback.message.message_id
    await state.update_data(id_message=id_message)
    await state.set_state(SignUpFSM.name)
    logger.debug('Send message from handler get_name')
    logger.debug('Change State to name')


@router.message(StateFilter(SignUpFSM.name), F.text.isalpha())
async def get_phone(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(name=message.text)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text=lexicon.REG_PHONE)

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.check_data)
    logger.debug('Send message from handler get_phone')
    logger.debug('Change State to phone')


@router.message(StateFilter(SignUpFSM.check_data))
async def creating_and_check(message: Message, state: FSMContext, bot: Bot):

    await state.update_data(phone=message.text)
    adjust = (2, 2)
    keyboard = create_inline_kb(adjust, **accept_cancel)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    await state.update_data(comment=message.text)
    sent_message = await message.answer(
        text=lexicon.REG_CREATE,
        reply_markup=keyboard)

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.accept_session)
    logger.debug('Send message from handler creating_and_check')
    logger.debug('Change State to accept_session')


@router.callback_query(StateFilter(SignUpFSM.accept_session),
                       CheckCallbackAccept())
async def accept_creating(callback: types.CallbackQuery, state: FSMContext,
                          session: Session):

    await callback.message.delete()
    data_for_request = await state.get_data()
    response = await create_session_api(data_for_request)
    response_data = response.json()
    if response.status_code == 201:
        record_hash = response_data['data'][0]['record_hash']
        record_id = response_data['data'][0]['record_id']
        await state.update_data(record_hash=record_hash)
        await state.update_data(record_id=record_id)
        data = await state.get_data()
        data_for_db = create_registration_for_db(data)
        add_record_in_db(session, data_for_db)
        ycl_id = get_ycl_id(data)
        telegram_id = callback.from_user.id
        await state.update_data(ycl_id=ycl_id)
        await state.update_data(telegram_id=telegram_id)
        data = await state.get_data()
        add_client_in_db(session, data)

        state_data = await state.get_data()
        staff_name = state_data['staff_name']
        service_title = state_data['service_title']
        date = state_data['date']
        date = to_normalize_date(date)
        time = state_data['time']

        await callback.answer(text=lexicon.REG_ACCEPT_FINAL)
        await callback.message.answer(
            text=lexicon.REG_FINAL.format(staff_name, service_title, date,
                                          time)
        )
        await state.clear()
        logger.debug('Send message from handler accept_creating')
        logger.debug('Change State to default_state')
        logger.debug(
            "Отправлен POST-запрос на создание записи.\n"
            f'Ответ: {response.json()}')
    elif response.status_code == 422:
        message = response_data['meta']['message']
        await callback.message.answer(
            text=message
        )
        await state.clear()


@router.message(F.text == 'Отмена')
async def cancel_creating(message: Message, state: FSMContext):

    keyboard = create_kb(start_buttons['adjust'], *start_buttons['buttons'])

    await message.answer(text=lexicon.REG_MAIN_CANCEL, reply_markup=keyboard)
    await state.clear()

    logger.debug('Send message from handler cancel_creating')
    logger.debug('Change State to default_state')
