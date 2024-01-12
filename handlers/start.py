from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.keyboards import create_inline_kb
from utils.strings import START_MESSAGE

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    keyboard = create_inline_kb(3, 'btn_1', 'btn_2', 'btn_3', 'btn_4', 'btn_5')
    await message.answer(
        text=START_MESSAGE,
        reply_markup=keyboard
    )
