import datetime
import logging

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from api.auth import send_sms_code, auth
from states.states import Auth
from filters.filters import CheckCallbackAuth
from utils.utils_db import check_exist_client_in_db

logger = logging.getLogger(__name__)

router = Router()


current_year = datetime.datetime.now().year


@router.message(F.text == 'Авторизоваться 🔑')
async def ask_phone(message: Message, state: FSMContext, session):

    telegram_id = message.from_user.id

    user_auth = check_exist_client_in_db(session, telegram_id)
    if not user_auth:
        await message.delete()
        sent_message = await message.answer(text='Введите свой номер телефона в формате 79991234567:')
        sent_message_id = sent_message.message_id
        await state.update_data(id_message=sent_message_id)

        await state.set_state(Auth.waiting_phone)
    else:
        await message.answer(text='Вы уже авторизованы!')


@router.callback_query(CheckCallbackAuth())
async def ask_phone_callback(callback, state: FSMContext, session):

    telegram_id = callback.message.from_user.id

    user_auth = check_exist_client_in_db(session, telegram_id)
    if not user_auth:
        await callback.message.edit_text(text='Введите свой номер телефона в формате 79991234567:')
        sent_message_id = callback.message.message_id
        await state.update_data(id_message=sent_message_id)

        await state.set_state(Auth.waiting_phone)
    else:
        await callback.message.edit_text(text='Вы уже авторизованы!')


@router.message(StateFilter(Auth.waiting_phone))
async def get_phone_ask_name(message: Message, state: FSMContext, bot):

    phone = message.text
    await state.update_data(phone=phone)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text='Введите свое имя: ')
    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(Auth.waiting_name)


@router.message(StateFilter(Auth.waiting_name))
async def get_name_send_code(message: Message, state: FSMContext, bot):

    name = message.text
    await state.update_data(name=name)

    state_data = await state.get_data()
    phone = state_data['phone']
    send_sms_code(phone, name)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text='Вам отправлен код авторизации. Проверьте ваши WhatsApp и сообщения, и введите код: ')
    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(Auth.waiting_code)


@router.message(StateFilter(Auth.waiting_code))
async def get_code(message: Message, state: FSMContext, session, bot):

    state_data = await state.get_data()
    name = state_data['name']
    phone = state_data['phone']
    code = message.text
    telegram_id = message.from_user.id

    result = auth(session, name, phone, code, telegram_id)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    if result['success'] is True:
        await message.answer(
            text='Вы авторизованы! ✅')
    if result['success'] is False:
        await message.answer(
            text='Ошибка! ❌')

    await state.clear()
