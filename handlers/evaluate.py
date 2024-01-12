from typing import Union

from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from fastapi.api_functions import send_to_api
from handlers.start import create_inline_kb
from utils.strings import LETTER_ONE, LETTER_TWO, LETTER_THREE, ERROR, RESTART_MESSAGE, WAITING_MESSAGE

router = Router()


class FSMFillForm(StatesGroup):
    waiting_for_text_input = State()


@router.callback_query(F.data.startswith('email'), StateFilter(default_state))
async def msg_display_letter(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)

    letter = LETTER_ONE
    if callback.data == 'email_2':
        letter = LETTER_TWO
    elif callback.data == 'email_3':
        letter = LETTER_THREE

    await state.update_data(chosen_letter=letter)
    await callback.message.answer(text=letter)
    await state.set_state(FSMFillForm.waiting_for_text_input)


@router.message(StateFilter(FSMFillForm.waiting_for_text_input))
async def process_text_input(message: types.Message, state: FSMContext):

    await message.answer(WAITING_MESSAGE)

    user_data = await state.get_data()
    chosen_letter = user_data['chosen_letter']
    await state.update_data(user_text=message.text)

    # Подключение к API
    evaluation_result = await send_to_api(message.text, letter=chosen_letter)

    keyboard = create_inline_kb(1, 'btn_6', 'btn_7', 'btn_8', 'btn_9')

    if evaluation_result == ERROR:
        await message.answer(evaluation_result, reply_markup=keyboard)
    else:
        await message.answer(f"Ваш результат:\nРешение коммуникативной задачи: {evaluation_result} из 2 баллов",
                             reply_markup=keyboard)

    await state.set_state(state=None)


@router.callback_query(F.data == 'get_comments')
async def get_comments(callback: CallbackQuery):
    await callback.message.answer(text='Здесь будут выведены комментарии')


@router.callback_query(F.data == 'view_my_work')
async def view_my_work(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    user_text = user_data['user_text']

    await callback.message.answer(text=f'Ваша работа: \n{user_text}')


async def start_over(event: Union[types.Message, CallbackQuery]):

    keyboard = create_inline_kb(3, 'btn_1', 'btn_2', 'btn_3')

    if isinstance(event, types.Message):
        await event.answer(
            text=RESTART_MESSAGE,
            reply_markup=keyboard
        )
    elif isinstance(event, CallbackQuery):
        await event.message.answer(
            text=RESTART_MESSAGE,
            reply_markup=keyboard
        )
router.message(Command("evaluate"))(start_over)
router.callback_query(F.data == 'restart')(start_over)
