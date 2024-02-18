import os
from abc import ABC
from unittest.mock import patch, AsyncMock

import pytest
from aiogram import F, Bot
from aiogram.filters import Command, Filter
from dotenv import load_dotenv

from .aiogram_tests import MockedBot
from .aiogram_tests.handler import MessageHandler, CallbackQueryHandler
from .aiogram_tests.types.dataset import MESSAGE, CALLBACK_QUERY
from handlers import rate
from handlers.rate import FSMFillForm, send_feedback_to_developer
from utils.strings import RATE_BOT, ASK_FOR_RECOMMENDATIONS, THANKS, SKIP


load_dotenv('.env')


class EnvConfig:
    bot_token = os.getenv("BOT_TOKEN")
    developer_id_1 = int(os.getenv("DEVELOPER_ID_1"))
    developer_id_2 = int(os.getenv("DEVELOPER_ID_2"))


class MockFilter(Filter, ABC):
    def __init__(self, check):
        self.check = check

    async def __call__(self, message):
        return self.check(message)


@pytest.mark.asyncio
async def test_rate_this_bot():
    requester = MockedBot(MessageHandler(rate.rate_this_bot, Command("rate")))
    calls = await requester.query(MESSAGE.as_object(text="/rate"))

    request = requester.get_last_request()
    assert hasattr(request, 'reply_markup')
    assert request.reply_markup.resize_keyboard

    answer_message = calls.send_message.fetchone()
    assert answer_message.text == RATE_BOT


@pytest.mark.asyncio
async def test_rate_button_pressed():
    mock_message = MESSAGE.as_object(text="rate")
    mock_callback = CALLBACK_QUERY.as_object(message=mock_message, data='rate')
    requester = MockedBot(CallbackQueryHandler(rate.rate_button_pressed, F.data.startswith('rate')))
    calls = await requester.query(mock_callback)
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == RATE_BOT


@pytest.mark.asyncio
async def test_rate():
    is_digit_and_in_range = MockFilter(lambda message: message.text.isdigit() and 1 <= int(message.text) <= 5)
    requester = MockedBot(
        MessageHandler(rate.rate, is_digit_and_in_range, state=FSMFillForm.waiting_for_recommendations))
    calls = await requester.query(MESSAGE.as_object(text="5"))
    request = requester.get_last_request()
    assert hasattr(request, 'reply_markup')
    assert request.reply_markup.resize_keyboard
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == ASK_FOR_RECOMMENDATIONS


@pytest.mark.asyncio
async def test_get_recommendations():
    mock_message = MESSAGE.as_object(text="Бот - огонь!")

    is_not_skip = MockFilter(lambda message: message.text != SKIP)
    requester = MockedBot(
        MessageHandler(rate.get_recommendations, is_not_skip, state=FSMFillForm.waiting_for_recommendations))

    with patch('handlers.rate.send_feedback_to_developer', new_callable=AsyncMock) as mock_send_feedback, \
            patch('aiogram.fsm.context.FSMContext.get_data', new_callable=AsyncMock) as mock_get_data:
        mock_get_data.return_value = {'rating': 5, 'recommendations': "Бот - огонь!"}

        calls = await requester.query(mock_message)
        request = requester.get_last_request()
        assert request.reply_markup.remove_keyboard
        answer_message = calls.send_message.fetchone()
        assert answer_message.text == THANKS

        mock_send_feedback.assert_called_once_with(requester._handler.bot, mock_message.from_user.id, 5, "Бот - огонь!")


@pytest.mark.asyncio
async def test_skip_recommendations():
    mock_message = MESSAGE.as_object(text=SKIP)

    is_skip = MockFilter(lambda message: message.text == SKIP)
    requester = MockedBot(
        MessageHandler(rate.skip_recommendations, is_skip, state=FSMFillForm.waiting_for_recommendations))

    with patch('handlers.rate.send_feedback_to_developer', new_callable=AsyncMock) as mock_send_feedback, \
            patch('aiogram.fsm.context.FSMContext.get_data', new_callable=AsyncMock) as mock_get_data:
        mock_get_data.return_value = {'rating': 5}

        calls = await requester.query(mock_message)
        request = requester.get_last_request()
        assert request.reply_markup.remove_keyboard
        answer_message = calls.send_message.fetchone()
        assert answer_message.text == THANKS

        mock_send_feedback.assert_called_once_with(requester._handler.bot, mock_message.from_user.id, 5)


@pytest.mark.asyncio
async def test_send_feedback_to_developer():
    with patch('aiogram.Bot.send_message', new_callable=AsyncMock) as mock_send_message, \
            patch('handlers.rate.config', new=EnvConfig):
        bot = Bot(EnvConfig.bot_token)

        await send_feedback_to_developer(bot, 12345678, 5, "Бот - огонь!")

        # Проверяем, что send_message был вызван два раза (по одному разу для каждого разработчика)
        assert mock_send_message.call_count == 2

        expected_message = "Пользователь с ID 12345678 поставил мне 5 и оставил следующую рекомендацию: Бот - огонь!"
        mock_send_message.assert_any_call(EnvConfig.developer_id_1, expected_message)
        mock_send_message.assert_any_call(EnvConfig.developer_id_2, expected_message)
