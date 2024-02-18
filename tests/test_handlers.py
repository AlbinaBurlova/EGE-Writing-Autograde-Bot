import json

import pytest
from aiogram.filters import Command

from .aiogram_tests import MockedBot
from .aiogram_tests.handler import MessageHandler
from .aiogram_tests.types.dataset import MESSAGE
from handlers import get_secret, other_handlers, start, help
from utils.keyboards import create_inline_kb
from utils.strings import SECRET, SEND_TO_MENU, START_MESSAGE, HELP_MESSAGE


@pytest.mark.asyncio
async def test_start_command():
    requester = MockedBot(MessageHandler(start.start_command, Command("start")))
    calls = await requester.query(MESSAGE.as_object(text="/start"))

    request = requester.get_last_request()
    assert hasattr(request, 'reply_markup')
    assert json.loads(request.reply_markup.json()) == json.loads(
        create_inline_kb(3, 'btn_1', 'btn_2', 'btn_3', 'btn_4', 'btn_5').model_dump_json())

    answer_message = calls.send_message.fetchone()
    assert answer_message.text == START_MESSAGE


@pytest.mark.asyncio
async def test_show_help_message():
    requester = MockedBot(MessageHandler(help.show_help_message, Command("help")))
    calls = await requester.query(MESSAGE.as_object(text="/help"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == HELP_MESSAGE


@pytest.mark.asyncio
async def test_show_secret():
    requester = MockedBot(MessageHandler(get_secret.show_secret, Command(commands=["secret"])))
    calls = await requester.query(MESSAGE.as_object(text="/secret"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == SECRET


@pytest.mark.asyncio
async def test_other_handlers():
    requester = MockedBot(MessageHandler(other_handlers.send_to_menu))
    calls = await requester.query(MESSAGE.as_object(text="Эй, ты!"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == SEND_TO_MENU
