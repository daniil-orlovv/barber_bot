import datetime

from aiogram import Bot, F, types, Router
from aiogram.types import Message
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config_data.config import location, TIME, PHONE, ADDRESS
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
async def process_start_command(message: Message, state: FSMContext):

    buttons = ['Контакты', 'Записаться', 'Отменить запись']
    adjust = (2, 1)
    keyboard = create_kb(adjust, *buttons)
    await message.answer(
        text='Привет!\nЯ бот Максуда!'
             '\nДавай запишу тебя на стрижку!',
        reply_markup=keyboard
    )


@router.message(F.text == 'Контакты')
async def command_contacts(message: Message):
    await message.answer_location(
        location.latitude,
        location.longitude
    )
    await message.answer(f'{ADDRESS}\n{TIME}\n{PHONE}')


@router.message(StateFilter(default_state), F.text == 'Записаться')
async def command_sign_up(message: Message, state: FSMContext):

    free_staffs = get_free_staff()
    inverted_staffs = {v: k for k, v in free_staffs.items()}

    await state.update_data(all_staffs=inverted_staffs)
    adjust = (2, 2, 2)
    keyboard_inline = create_inline_kb(adjust, **free_staffs)
    await message.delete()

    await message.answer(
        text='Выбери мастера:',
        reply_markup=keyboard_inline
    )
    await state.set_state(SignUpFSM.staff)


@router.callback_query(CheckFreeStaff(), StateFilter(SignUpFSM.staff))
async def send_choose_service(
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

    adjust = (2, 2, 2)
    keyboard_services = create_inline_kb(adjust, **free_services)

    await callback.message.edit_text(
        text=(f"Ваш мастер: {staff_name}\n\n"
              f"Выбери услугу:"),
        reply_markup=keyboard_services
    )
    await state.set_state(SignUpFSM.service)


@router.callback_query(StateFilter(SignUpFSM.service), CheckFreeService())
async def send_choose_date(callback: types.CallbackQuery, state: FSMContext):

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
        text=(f'Ваш мастер: {staff_name}\n'
              f'Ваша услуга: {service_title}\n\n'
              f'Выбери дату:'),
        reply_markup=keyboard
    )
    await state.set_state(SignUpFSM.date)


@router.callback_query(StateFilter(SignUpFSM.date), CheckFreeDate())
async def send_choosing_time(callback: types.CallbackQuery, state: FSMContext):

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
        text=(f'Ваш мастер: {staff_name}\n'
              f'Ваша услуга: {service_title}\n'
              f'Дата: {norm_date}\n\n'
              f'Выбери время:'),
        reply_markup=keyboard_times
    )
    await state.set_state(SignUpFSM.time)


@router.callback_query(StateFilter(SignUpFSM.time), CheckFreeTime())
async def send_choise_of_user(
    callback: types.CallbackQuery,
    state: FSMContext
):

    await state.update_data(time=callback.data)
    state_data = await state.get_data()
    staff_name = state_data['staff_name']
    service_title = state_data['service_title']
    date = state_data['date']

    buttons = {
        'Подтвердить': 'accept',
        'Отменить': 'cancel',
        'Изменить': 'edit'
    }
    adjust = (2, 1)
    keyboard = create_inline_kb(adjust, **buttons)

    await callback.message.edit_text(
        text=(f'Ваш мастер: {staff_name}\n'
              f'Ваша услуга: {service_title}\n'
              f'Дата: {to_normalize_date(date)}\n'
              f'Время: {callback.data}\n\n'
              f'Все верно?'),
        reply_markup=keyboard
    )
    await state.set_state(SignUpFSM.check_data)


@router.callback_query(StateFilter(SignUpFSM.check_data),
                       lambda callback: callback.data == 'cancel')
async def process_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Вы отменили процесс записи.'
    )
    await state.clear()


@router.callback_query(StateFilter(SignUpFSM.check_data),
                       lambda callback: callback.data == 'accept')
async def process_accept(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text='Спасибо, теперь введите свое имя:')
    id_message = callback.message.message_id
    await state.update_data(id_message=id_message)
    await state.set_state(SignUpFSM.name)


@router.message(StateFilter(SignUpFSM.name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text='А теперь введите ваш телефон в формате 79000000000:')

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.phone)


@router.message(StateFilter(SignUpFSM.phone))
async def process_phone_sent(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text='Введите ваш email в формате mail@mail.ru:')

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.email)


@router.message(StateFilter(SignUpFSM.email))
async def process_email_sent(message: Message, state: FSMContext):
    await state.update_data(email=message.text)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text='Возможно, есть какие-то комментарии, укажите их:')

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.comment)


@router.message(StateFilter(SignUpFSM.comment))
async def create_session(message: Message, state: FSMContext):

    adjust = (2, 2)
    buttons = {'Подтвердить': 'accept',
               'Отменить': 'cancel'}
    keyboard = create_inline_kb(adjust, **buttons)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    await state.update_data(comment=message.text)
    sent_message = await message.answer(
        text='Спасибо!\n\n Создать запись на сеанс?',
        reply_markup=keyboard)

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.accept_session)


@router.callback_query(StateFilter(SignUpFSM.accept_session),
                       lambda callback: callback.data == 'accept')
async def accept_session(callback: types.CallbackQuery, state: FSMContext):

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
    time = state_data['time']

    await callback.answer(text='Запись создана!\n\n')
    await callback.message.answer(
        text=f'Вы записаны!\n\n'
             f'Ваш мастер: {staff_name}\n'
             f'Ваша услуга: {service_title}\n'
             f'Дата: {to_normalize_date(date)}\n'
             f'Время: {time}\n\n'
    )
    await state.clear()


@router.message(F.text == 'Отменить запись')
async def command_cancel(message: Message, state: FSMContext):

    buttons = ['Контакты', 'Записаться', 'Отменить запись']
    adjust = (2, 1)
    keyboard = create_kb(adjust, *buttons)

    await message.answer(
        text='Запись отменена!\n\nВыбери дейстие:',
        reply_markup=keyboard
    )
    await state.clear()
