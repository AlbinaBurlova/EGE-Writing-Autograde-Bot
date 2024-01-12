from aiogram import types, Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import Command


router = Router()


@router.message(Command("get_stat"))
async def show_stat(message: types.Message):
    await message.answer("Здесь будет выводиться статистика ответов")


@router.callback_query(F.data == "get_stat")
async def callback_show_stat(callback: CallbackQuery):
    await show_stat(callback.message)
    await callback.answer()
