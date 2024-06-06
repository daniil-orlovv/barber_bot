import time

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.keyboards_utils import create_inline_kb
from states.states import Feedback
from lexicon.buttons import accept_cancel
from filters.filters import CheckCallbackFeedback
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.get_feedback import feedback
from utils.utils_db import get_user_token_of_client
from sqlalchemy.orm import Session

router = Router()


async def get_feedback(bot, user_id):
    print('Запущена функция отправки кнопки для фидбека.')
    button = InlineKeyboardButton(
        text='Оставить отзыв',
        callback_data='feedback'
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[button]]
    )
    await bot.send_message(user_id,
                           text="Пожалуйста, оставьте отзыв о мастере.",
                           reply_markup=reply_markup)


@router.callback_query(CheckCallbackFeedback())
async def start_feedback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Загрузка... ⏳')
    sent_message = await callback.message.edit_text(
        text='Напишите ваше впечатление:'
    )
    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)
    await state.set_state(Feedback.waiting_text)


@router.message(F.text == 'Оставить отзыв мастеру 💇')
async def start_feedback_message(message, state: FSMContext):
    sent_message = await message.answer(
        text='Напишите ваше впечатление:'
    )
    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)
    await state.set_state(Feedback.waiting_text)


@router.message(StateFilter(Feedback.waiting_text))
async def get_text_feedback(message, state: FSMContext, bot):
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
    await state.set_state(Feedback.waiting_mark)


@router.callback_query(StateFilter(Feedback.waiting_mark))
async def get_mark_feedback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Загрузка... ⏳')
    mark = callback.data
    await state.update_data(mark=mark)

    await callback.message.edit_text(
        text='Укажите свое имя для отзыва:'
    )
    await state.set_state(Feedback.waiting_name)


@router.message(StateFilter(Feedback.waiting_name))
async def get_name_feedback(message, state: FSMContext):
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

    await state.set_state(Feedback.waiting_accepting)


@router.callback_query(StateFilter(Feedback.waiting_accepting))
async def acceptng_feedback(callback: types.CallbackQuery, session: Session,
                            state: FSMContext):

    if callback.data == 'accept':
        await callback.message.edit_text('Отправляю отзыв... ⏳')

        state_data = await state.get_data()
        text = state_data['text']
        mark = state_data['mark']
        name = state_data['name']
        print(name, text, mark)
        telegram_id = callback.from_user.id
        user_token = get_user_token_of_client(session, telegram_id)
        feedback(mark, text, name, user_token)

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
