from aiogram import types, Router
from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.strings import RATE_BOT, ASK_FOR_RECOMMENDATIONS, SKIP, THANKS

# TODO: определиться с тем, где храним данные: оценку пользователи и рекомендации

router = Router()


class FSMFillForm(StatesGroup):
    waiting_for_recommendations = State()


@router.message(Command("rate"), StateFilter(default_state))
async def rate_this_bot(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 6):
        builder.add(types.KeyboardButton(text=str(i)))
    await message.answer(RATE_BOT, reply_markup=builder.as_markup(resize_keyboard=True))

    await state.set_state(FSMFillForm.waiting_for_recommendations)


@router.callback_query(F.data.startswith('rate'))
async def rate_button_pressed(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await rate_this_bot(callback.message, state)


@router.message(lambda message: message.text.isdigit() and 1 <= int(message.text) <= 5,
                StateFilter(FSMFillForm.waiting_for_recommendations))
async def rate(message: types.Message, state: FSMContext):
    await state.update_data(rating=int(message.text))

    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text=SKIP))

    await message.answer(ASK_FOR_RECOMMENDATIONS, reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(F.text != SKIP, StateFilter(FSMFillForm.waiting_for_recommendations))
async def get_recommendations(message: types.Message, state: FSMContext):
    await state.update_data(recommendations=message.text)
    await message.answer(THANKS, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(state=None)


@router.message(F.text == SKIP, StateFilter(FSMFillForm.waiting_for_recommendations))
async def skip_recommendations(message: types.Message, state: FSMContext):
    await message.answer(THANKS, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(state=None)
