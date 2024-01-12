from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.strings import SECRET


router = Router()


@router.message(Command("secret"))
async def show_secret(message: Message):
    await message.answer(SECRET)
