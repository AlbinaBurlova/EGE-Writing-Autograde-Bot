from typing import Union
import asyncio

from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from fast_api.api_functions import send_to_api
from handlers.start import create_inline_kb
from utils.strings import LETTER_ONE, LETTER_TWO, LETTER_THREE, RESTART_MESSAGE, WAITING_MESSAGE, TRY_AGAIN
from handlers.get_stat import results


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

    try:
        # Подключение к API
        evaluation_result = await send_to_api(message.text, letter=chosen_letter)
        await state.update_data(result=evaluation_result)
        results.append(evaluation_result)
        keyboard = create_inline_kb(1, 'btn_6', 'btn_7', 'btn_8', 'btn_9')
        await message.answer(f"Ваш результат: {evaluation_result['total']} из 6 баллов",
                             reply_markup=keyboard)

    except Exception as e:
        await message.answer(TRY_AGAIN)
        await asyncio.sleep(3)
        await start_over(message)
        await state.set_state(state=None)
        return

    await state.set_state(state=None)


@router.callback_query(F.data == 'get_comments')
async def get_comments(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    evaluation_result = user_data['result']
    print(evaluation_result)

    await callback.message.answer(text=f'Решение коммуникативной задачи: {evaluation_result["k1"]} из 2 баллов.\nОрганизация текста: {evaluation_result["k2"]} из 2 баллов.\nЯзыковое оформление текста: {evaluation_result["k3"]} из 2 баллов.\n{evaluation_result["comments"]}')


async def start_over(event: Union[types.Message, CallbackQuery]):

    keyboard = create_inline_kb(3, 'btn_1', 'btn_2', 'btn_3')
    await event.bot.send_message(
        chat_id=event.from_user.id,
        text=RESTART_MESSAGE,
        reply_markup=keyboard
    )

router.message(Command("evaluate"))(start_over)
router.callback_query(F.data == 'restart')(start_over)

