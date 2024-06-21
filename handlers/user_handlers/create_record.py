import datetime
import logging
import time

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session

from api.check_record import check_record_for_create
from api.create_record import (create_record, get_free_date, get_free_services,
                               get_free_staff, get_free_time)
from filters.filters import (CheckCallbackAccept, CheckCallbackCancel,
                             CheckCallbackRecreateRecord, CheckFreeDate,
                             CheckFreeService, CheckFreeStaff, CheckFreeTime)
from handlers.user_handlers.schedulers import create_jobs
from keyboards.keyboards_utils import (create_calendar, create_inline_kb,
                                       create_kb)
from lexicon import lexicon_ru as lexicon
from lexicon.buttons import accept_cancel, recreate_record, start_buttons
from states.states import SignUpFSM
from utils.utils import to_normalize_date

logger = logging.getLogger(__name__)

router = Router()


current_year = datetime.datetime.now().year


@router.message(CommandStart())
async def start(message: Message) -> None:
    """Хэндлер реагирует на команду /start и отправляет приветствие и
    клавиатуру пользователю."""

    keyboard = create_kb(start_buttons['adjust'], *start_buttons['buttons'])
    await message.answer(text=lexicon.WELCOME_TEXT, reply_markup=keyboard)


@router.message(F.text == 'Записаться ✏️')
async def send_masters(message: Message, state: FSMContext) -> None:
    """Хэндлер реагирует на кнопку с надписью 'Записаться ✏️' и отправляет
    инлайн-клавиатуру пользователю с сотрудниками на выбор."""

    free_staffs = get_free_staff()
    inverted_staffs = {v: k for k, v in free_staffs.items()}

    adjust = (2, 2, 2)
    keyboard_inline = create_inline_kb(adjust, **free_staffs)

    await message.delete()
    await message.answer(text=lexicon.REG_MASTER, reply_markup=keyboard_inline)

    await state.update_data(all_staffs=inverted_staffs)
    await state.set_state(SignUpFSM.staff)


@router.callback_query(CheckCallbackRecreateRecord())
async def send_masters_recreate(callback: CallbackQuery,
                                state: FSMContext) -> None:
    """Хэндлер реагирует на callback='recreate' и запускает цепочку записи по
    новой, предлагая сотрудников для пользователя, как и хэндлер выше."""

    free_staffs = get_free_staff()
    inverted_staffs = {v: k for k, v in free_staffs.items()}

    adjust = (2, 2, 2)
    keyboard_inline = create_inline_kb(adjust, **free_staffs)

    await callback.message.edit_text(
        text=lexicon.REG_MASTER, reply_markup=keyboard_inline)

    await state.update_data(all_staffs=inverted_staffs)
    await state.set_state(SignUpFSM.staff)


@router.callback_query(CheckFreeStaff(), StateFilter(SignUpFSM.staff))
async def send_service(callback: CallbackQuery,
                       state: FSMContext) -> None:
    """Хэндлер проверяет совпадение callback и результата запроса на
    сотрудников по api, реагирует на состояние SignUpFSM.staff, получает и
    запоминает сотрудника, которого выбрал пользователь. Отправляет услуги,
    связанные с этим сотрудником, пользователю."""

    await callback.message.edit_text('Ищу доступные услуги... ⏳')
    staff_id = callback.data
    state_data = await state.get_data()
    all_staffs = state_data.get('all_staffs', {})
    staff_name = all_staffs.get(staff_id)
    await state.update_data(staff_name=staff_name, staff_id=staff_id)

    free_services = get_free_services(staff_id)
    inverted_services = {v: k for k, v in free_services.items()}
    await state.update_data(all_services=inverted_services)

    adjust = (1, 1)
    keyboard_services = create_inline_kb(adjust, **free_services)

    time.sleep(0.5)
    await callback.message.edit_text(
        text=lexicon.REG_SERVICE.format(staff_name),
        reply_markup=keyboard_services
    )
    await state.set_state(SignUpFSM.service)


@router.callback_query(StateFilter(SignUpFSM.service), CheckFreeService())
async def send_date(callback: CallbackQuery, state: FSMContext) -> None:
    """Хэндлер проверяет совпадение callback и результата запроса на
    услуги по api, реагирует на состояние SignUpFSM.service, получает и
    запоминает услугу, которую выбрал пользователь. Отправляет свободные даты,
    связанные с этой услугой, пользователю."""

    await callback.message.edit_text('Ищу свободные даты... ⏳')
    service_id = callback.data
    state_data = await state.get_data()
    staff_id = state_data['staff_id']
    staff_name = state_data['staff_name']

    all_services = state_data.get('all_services', {})
    service_title = all_services.get(service_id)
    await state.update_data(service_title=service_title, service_id=service_id)

    free_days = get_free_date(staff_id)
    keyboard = create_calendar(free_days)

    time.sleep(0.5)
    await callback.message.edit_text(
        text=lexicon.REG_DATE.format(staff_name, service_title),
        reply_markup=keyboard
    )
    await state.set_state(SignUpFSM.date)


@router.callback_query(StateFilter(SignUpFSM.date), CheckFreeDate())
async def send_time(callback: CallbackQuery, state: FSMContext) -> None:
    """Хэндлер проверяет совпадение callback и результата запроса на
    даты по api, реагирует на состояние SignUpFSM.date, получает и
    запоминает дату, которую выбрал пользователь. Отправляет свободное время,
    связанное с этой датой, пользователю."""

    await callback.message.edit_text('Ищу свободное время... ⏳')
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

    time.sleep(0.5)
    await callback.message.edit_text(
        text=lexicon.REG_TIME.format(staff_name, service_title, norm_date),
        reply_markup=keyboard_times
    )
    await state.set_state(SignUpFSM.time)


@router.callback_query(StateFilter(SignUpFSM.time), CheckFreeTime())
async def pre_check(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """Хэндлер проверяет совпадение callback и результата запроса на
    время по api, реагирует на состояние SignUpFSM.time, получает и
    запоминает время, которое выбрал пользователь. Отправляет
    инлайн-клавиатуру с подтверждением/отменой данных о записи."""

    await callback.message.edit_text('Загрузка... ⏳')
    await state.update_data(time=callback.data)
    state_data = await state.get_data()
    staff_name = state_data['staff_name']
    service_title = state_data['service_title']
    date = state_data['date']
    date = to_normalize_date(date)
    times = state_data['time']

    adjust = (2, 1)
    keyboard = create_inline_kb(adjust, **accept_cancel)

    time.sleep(0.5)
    await callback.message.edit_text(
        text=lexicon.REG_CHECK.format(staff_name, service_title, date, times),
        reply_markup=keyboard
    )
    await state.set_state(SignUpFSM.check_data)


@router.callback_query(StateFilter(SignUpFSM.check_data),
                       CheckCallbackCancel())
async def cancel(callback: CallbackQuery, state: FSMContext) -> None:
    """Хэндлер реагирует на состояние SignUpFSM.check_data, и проверяет
    совпадение callbcak с 'cancel'. Отменяет процесс записи."""

    await callback.message.edit_text('Загрузка... ⏳')
    time.sleep(0.5)
    await callback.message.edit_text(
        text='Вы отменили процесс записи.'
    )
    await state.clear()


@router.callback_query(StateFilter(SignUpFSM.check_data),
                       CheckCallbackAccept())
async def get_name(callback: CallbackQuery, state: FSMContext) -> None:
    """Хэндлер реагирует на состояние SignUpFSM.check_data, и проверяет
    совпадение callbcak с 'accept'. Проверяет возможность создания записи с
    такими данными с помощью запроса по api. Если все в порядке, то
    запрашивает имя пользователя для создания записи. Если нет - уведомляет
    пользователя и отправляет инлайн-клавиатуру с возможностью отменить
    запись или изменить ее данные."""

    state_data = await state.get_data()
    response = check_record_for_create(state_data)
    if response.status_code == 201:
        await callback.message.edit_text('Загрузка... ⏳')
        time.sleep(0.5)
        await callback.message.edit_text(
            text=lexicon.REG_NAME)
        id_message = callback.message.message_id
        await state.update_data(id_message=id_message)
        await state.set_state(SignUpFSM.name)
    elif response.status_code == 422:
        response_data = response.json()
        message = response_data['meta']['message']
        adjust = (2, 2)
        keyboard = create_inline_kb(adjust, **recreate_record)
        await callback.message.edit_text(
            text=message,
            reply_markup=keyboard
        )
        await state.clear()


@router.message(StateFilter(SignUpFSM.name), F.text.isalpha())
async def get_phone(message: Message, state: FSMContext, bot: Bot) -> None:
    """Хэндлер реагирует на состояние SignUpFSM.name и наличие букв в
    сообщении. Получает и запоминает имя пользователя для записи."""

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


@router.message(StateFilter(SignUpFSM.check_data))
async def creating_and_check(message: Message, state: FSMContext,
                             bot: Bot) -> None:
    """Хэндлер реагирует на состояние SignUpFSM.check_data и наличие букв в
    сообщении. Получает, проверяет и запоминает номер пользователя для
    записи."""

    phone = message.text
    if not phone.isdigit() or not phone.startswith('7') or len(phone) != 11:
        await message.answer(
            text='Неправильный формат номера телефона. Попробуйте еще раз.')
        return
    await state.update_data(phone=phone)
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


@router.callback_query(StateFilter(SignUpFSM.accept_session),
                       CheckCallbackAccept())
async def accept_creating(callback: CallbackQuery, state: FSMContext,
                          session: Session, scheduler: AsyncIOScheduler,
                          bot: Bot) -> None:
    """Хэндлер реагирует на состояние SignUpFSM.accept_session и на наличие
    'accept' в callback. Создает запись на сеанс. Если неуспешно, то выводит
    информацию."""

    await callback.message.edit_text('Записываю на сеанс... ⏳')
    state_data = await state.get_data()
    response = await create_record(state_data)
    create_jobs(scheduler, bot, state_data, callback)

    response_data = response.json()
    if response.status_code == 201:

        state_data = await state.get_data()
        staff_name = state_data['staff_name']
        service_title = state_data['service_title']
        date = state_data['date']
        date = to_normalize_date(date)
        times = state_data['time']

        time.sleep(0.5)
        await callback.answer(text=lexicon.REG_ACCEPT_FINAL)
        await callback.message.edit_text(
            text=lexicon.REG_FINAL.format(staff_name, service_title, date,
                                          times)
        )
        await state.clear()
    elif response.status_code == 422:
        message = response_data['meta']['message']
        await callback.message.answer(
            text=message
        )
        await state.clear()


@router.message(F.text == 'Отмена ❌')
async def cancel_creating(message: Message, state: FSMContext) -> None:
    """Хэндлер реагирует на кнопку с надписью 'Отмена ❌' и отменяет все любые
    действия пользователя и перебрасывает в главное меню."""

    keyboard = create_kb(start_buttons['adjust'], *start_buttons['buttons'])

    await message.answer(text=lexicon.REG_MAIN_CANCEL, reply_markup=keyboard)
    await state.clear()
