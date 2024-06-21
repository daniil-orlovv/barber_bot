import time

from aiogram import Bot, F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session

from api.get_feedback import get_feedback_company
from keyboards.keyboards_utils import create_inline_kb
from lexicon.buttons import accept_cancel, button_auth
from states.states import FeedbackCompany
from utils.utils_db import check_exist_client_in_db, get_user_token_of_client

router = Router()


@router.message(F.text == 'Оставить отзыв барбершопу ✂️')
async def start_feedback_message(message: Message, state: FSMContext,
                                 session: Session) -> None:
    """Хэндлер реагирует на кнопку с надписью 'Оставить отзыв барбершопу ✂️'
    , проверяет, авторизован ли пользователь, и отправляет просьбу написать
    свое впечатление."""

    telegram_id = message.from_user.id

    user_auth = check_exist_client_in_db(session, telegram_id)
    if user_auth:
        sent_message = await message.answer(
            text='Напишите ваше впечатление:'
        )
        sent_message_id = sent_message.message_id
        await state.update_data(id_message=sent_message_id)
        await state.set_state(FeedbackCompany.waiting_text)
    else:
        adjust = (1,)
        inline_keyboard = create_inline_kb(adjust, **button_auth)
        await message.answer(
                text=('Для того, чтобы оставить отзыв - необходимо'
                      'авторизоваться:'),
                reply_markup=inline_keyboard
            )


@router.message(StateFilter(FeedbackCompany.waiting_text))
async def get_text_feedback(message: Message, state: FSMContext,
                            bot: Bot) -> None:
    """Хэндлер реагирует на состояние FeedbackCompany.waiting_text,
    получает и сохраняет отзыв, просит поставить оценку с помощью
    инлайн-клавиатуры."""
    await state.update_data(text=message.text)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    marks = (1, 2, 3, 4, 5)
    adjust = (5,)
    inline_keyboard = create_inline_kb(adjust, *marks)
    await message.answer(
        text='Укажите оценку от 1 до 5:',
        reply_markup=inline_keyboard
    )
    await state.set_state(FeedbackCompany.waiting_mark)


@router.callback_query(StateFilter(FeedbackCompany.waiting_mark))
async def get_mark_feedback(callback: types.CallbackQuery,
                            state: FSMContext) -> None:
    """Хэндлер реагирует на состояние FeedbackCompany.waiting_mark,
    получает и сохраняет оценку, просит указать имя для отзыва."""
    await callback.message.edit_text('Загрузка... ⏳')
    mark = callback.data
    await state.update_data(mark=mark)

    await callback.message.edit_text(
        text='Укажите свое имя для отзыва:'
    )
    await state.set_state(FeedbackCompany.waiting_name)


@router.message(StateFilter(FeedbackCompany.waiting_name))
async def get_name_feedback(message: Message, state: FSMContext) -> None:
    """Хэндлер реагирует на состояние FeedbackCompany.waiting_name,
    получает и сохраняет имя, отправляет данные отзыва для подтверждения."""
    await state.update_data(name=message.text)
    state_data = await state.get_data()
    text = state_data['text']
    mark = state_data['mark']
    name = state_data['name']

    adjust = (2, 2)
    keyboard = create_inline_kb(adjust, **accept_cancel)
    await message.answer(
        text=(f'Проверьте отзыв и отправьте:\n'
              f'Текст отзыва: {text}\n'
              f'Ваша оценка: {mark}\n'
              f'Ваше имя: {name}'),
        reply_markup=keyboard
    )

    await state.set_state(FeedbackCompany.waiting_accepting)


@router.callback_query(StateFilter(FeedbackCompany.waiting_accepting))
async def acceptng_feedback(callback: types.CallbackQuery, session: Session,
                            state: FSMContext) -> None:
    """Хэндлер реагирует на состояние FeedbackCompany.waiting_accepting и
    отправляет, либо не отправляет отзыв, в зависимости от callback."""

    if callback.data == 'accept':
        await callback.message.edit_text('Отправляю отзыв... ⏳')

        state_data = await state.get_data()
        text = state_data['text']
        mark = state_data['mark']
        name = state_data['name']
        telegram_id = callback.from_user.id
        user_token = get_user_token_of_client(session, telegram_id)
        get_feedback_company(mark, text, name, user_token)

        time.sleep(0.5)
        await callback.message.edit_text(
            text='Отзыв отправлен! ✅'
        )
        await state.clear()

    elif callback.data == 'cancel':
        await callback.message.edit_text('Загрузка... ⏳')
        time.sleep(0.5)
        await callback.message.edit_text(
            text=('Отзыв не отправлен! Отправьте отзыв из главного меню'))
        await state.clear()
