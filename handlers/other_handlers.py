from aiogram import Router
from aiogram.types import Message
from utils.strings import SEND_TO_MENU


router = Router()


@router.message()
async def send_to_menu(message: Message):
    await message.answer(SEND_TO_MENU)
