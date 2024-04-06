import datetime

from aiogram import Bot, F, types, Router
from aiogram.types import Message
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config_data.config import (location, ADRESS_URL_GOOGLE, ADRESS_URL_YANDEX,
                                ADRESS_URL_2GIS)
from keyboards.keyboards_utils import (create_inline_kb, create_calendar,
                                       create_kb)
from external_services.yclients import (get_free_date, get_free_time,
                                        get_free_services, get_free_staff,
                                        create_session_api)
from utils.utils import create_registration_for_db, to_normalize_date
from models.models import Base
from filters.filters import (CheckFreeStaff, CheckFreeService, CheckFreeDate,
                             CheckFreeTime)
from config_data.config import load_config, Config
from states.states import SignUpFSM
import lexicon.lexicon_ru as lexicon
from lexicon.buttons import accept_cancel

config: Config = load_config()

bot = Bot(token=config.tg_bot.token,
          parse_mode='HTML')
router = Router()


current_year = datetime.datetime.now().year

# engine = create_engine(
#     "postgresql+psycopg2://admin:admin@localhost:5428/mydatabase")
engine = create_engine('sqlite:///sqlite3.db')
session = Session(bind=engine)
Base.metadata.create_all(engine)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):

    buttons = ['Контакты', 'Записаться', 'Отменить запись']
    adjust = (2, 1)
    keyboard = create_kb(adjust, *buttons)
    await message.answer(
        text=lexicon.WELCOME_TEXT,
        reply_markup=keyboard
    )


@router.message(F.text == 'Контакты')
async def contacts(message: Message):

    buttons = {
        'Открыть в Google картах': ADRESS_URL_GOOGLE,
        'Открыть в Яндекс картах': ADRESS_URL_YANDEX,
        'Открыть в 2ГИС': ADRESS_URL_2GIS
    }
    adjust = (1, 1, 1)
    inline_keyboard = create_inline_kb(adjust, **buttons)

    await message.answer_location(
        location.latitude,
        location.longitude
    )
    await message.answer(
        text=lexicon.ABOUT,
        reply_markup=inline_keyboard)


@router.message(StateFilter(default_state), F.text == 'Записаться')
async def reg_master(message: Message, state: FSMContext):

    free_staffs = get_free_staff()
    inverted_staffs = {v: k for k, v in free_staffs.items()}

    await state.update_data(all_staffs=inverted_staffs)
    adjust = (2, 2, 2)
    keyboard_inline = create_inline_kb(adjust, **free_staffs)
    await message.delete()

    await message.answer(
        text=lexicon.REG_MASTER,
        reply_markup=keyboard_inline
    )
    await state.set_state(SignUpFSM.staff)


@router.callback_query(CheckFreeStaff(), StateFilter(SignUpFSM.staff))
async def reg_service(
    callback: types.CallbackQuery,
    state: FSMContext
):
    staff_id = callback.data
    state_data = await state.get_data()
    all_staffs = state_data.get('all_staffs', {})
    staff_name = all_staffs.get(staff_id)
    await state.update_data(staff_name=staff_name)
    await state.update_data(staff_id=staff_id)

    free_services = get_free_services(staff_id)
    inverted_services = {v: k for k, v in free_services.items()}
    await state.update_data(all_services=inverted_services)

    adjust = [2, 2, 2]
    keyboard_services = create_inline_kb(adjust, **free_services)

    await callback.message.edit_text(
        text=lexicon.REG_SERVICE.format(staff_name),
        reply_markup=keyboard_services
    )
    await state.set_state(SignUpFSM.service)


@router.callback_query(StateFilter(SignUpFSM.service), CheckFreeService())
async def reg_date(callback: types.CallbackQuery, state: FSMContext):

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


@router.callback_query(StateFilter(SignUpFSM.date), CheckFreeDate())
async def reg_time(callback: types.CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    staff_name = state_data['staff_name']
    staff_id = state_data['staff_id']
    service_title = state_data['service_title']

    month, day = callback.data.split('-')
    date = f'{current_year}-{month}-{day}'
    await state.update_data(date=date)
    norm_date = to_normalize_date(callback.data)
    adjust = [4, 4, 4, 4, 4, 4,]
    free_times = get_free_time(staff_id, date)
    keyboard_times = create_inline_kb(adjust, *free_times)

    await callback.message.edit_text(
        text=lexicon.REG_TIME.format(staff_name, service_title, norm_date),
        reply_markup=keyboard_times
    )
    await state.set_state(SignUpFSM.time)


@router.callback_query(StateFilter(SignUpFSM.time), CheckFreeTime())
async def reg_check(
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

    adjust = [2, 1]
    keyboard = create_inline_kb(adjust, **accept_cancel)

    await callback.message.edit_text(
        text=lexicon.REG_CHECK.format(staff_name, service_title, date, time),
        reply_markup=keyboard
    )
    await state.set_state(SignUpFSM.check_data)


@router.callback_query(StateFilter(SignUpFSM.check_data),
                       lambda callback: callback.data == 'cancel')
async def reg_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Вы отменили процесс записи.'
    )
    await state.clear()


@router.callback_query(StateFilter(SignUpFSM.check_data),
                       lambda callback: callback.data == 'accept')
async def reg_name(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text=lexicon.REG_NAME)
    id_message = callback.message.message_id
    await state.update_data(id_message=id_message)
    await state.set_state(SignUpFSM.name)


@router.message(StateFilter(SignUpFSM.name), F.text.isalpha())
async def reg_phone(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text=lexicon.REG_PHONE)

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.phone)


@router.message(StateFilter(SignUpFSM.phone))
async def reg_mail(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text=lexicon.REG_MAIL)

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.email)


@router.message(StateFilter(SignUpFSM.email))
async def reg_comment(message: Message, state: FSMContext):
    await state.update_data(email=message.text)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text=lexicon.REG_COMMENT)

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.comment)


@router.message(StateFilter(SignUpFSM.comment))
async def reg_create(message: Message, state: FSMContext):

    adjust = [2, 2]
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


@router.callback_query(StateFilter(SignUpFSM.accept_session),
                       lambda callback: callback.data == 'accept')
async def reg_accept_final(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.delete()

    data_for_request = await state.get_data()
    await create_session_api(data_for_request)

    data_for_db = create_registration_for_db(data_for_request)
    session.add(data_for_db)
    session.commit()

    state_data = await state.get_data()
    staff_name = state_data['staff_name']
    service_title = state_data['service_title']
    date = state_data['date']
    date = to_normalize_date(date)
    time = state_data['time']

    await callback.answer(text=lexicon.REG_ACCEPT_FINAL)
    await callback.message.answer(
        text=lexicon.REG_FINAL.format(staff_name, service_title, date, time)
    )
    await state.clear()


@router.message(F.text == 'Отменить запись')
async def reg_main_cancel(message: Message, state: FSMContext):

    buttons = ['Контакты', 'Записаться', 'Отменить запись']
    adjust = (2, 1)
    keyboard = create_kb(adjust, *buttons)

    await message.answer(
        text=lexicon.REG_MAIN_CANCEL,
        reply_markup=keyboard
    )
    await state.clear()
