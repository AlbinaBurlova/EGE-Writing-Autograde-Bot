from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from utils.strings import HELP_MESSAGE


router = Router()


@router.message(Command("help"))
async def show_secret(message: Message):
    await message.answer(HELP_MESSAGE)
