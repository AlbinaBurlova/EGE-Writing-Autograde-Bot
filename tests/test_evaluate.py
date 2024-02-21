from unittest.mock import patch, AsyncMock

import pytest
from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup

from handlers.evaluate import msg_display_letter, process_text_input, start_over, view_my_work, \
    get_comments
from utils.strings import LETTER_TWO, ERROR, RESTART_MESSAGE, LETTER_THREE, LETTER_ONE
from .aiogram_tests import MockedBot
from .aiogram_tests.handler import CallbackQueryHandler, MessageHandler
from .aiogram_tests.types.dataset import MESSAGE, CALLBACK_QUERY


@pytest.mark.asyncio
async def test_msg_display_letter():
    handler = CallbackQueryHandler(msg_display_letter, F.data.startswith('email'))
    requester = MockedBot(handler)

    # Обработка случая с 'email_2'
    with patch('aiogram.fsm.context.FSMContext.update_data', new_callable=AsyncMock) as mock_update_data:
        await requester.query(CALLBACK_QUERY.as_object(data='email_2', message=MESSAGE.as_object(text="Йоу, бот!")))
        mock_update_data.assert_called_once_with(chosen_letter=LETTER_TWO)

    # Обработка случая с 'email_3'
    with patch('aiogram.fsm.context.FSMContext.update_data', new_callable=AsyncMock) as mock_update_data:
        await requester.query(CALLBACK_QUERY.as_object(data='email_3', message=MESSAGE.as_object(text="Йоу, бот!")))
        mock_update_data.assert_called_once_with(chosen_letter=LETTER_THREE)


class TestStates(StatesGroup):
    waiting_for_text_input = State()


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


@pytest.mark.asyncio
@pytest.mark.parametrize("evaluation_result, expected_message", [
    ({"total": 5, "k1": 1, "k2": 2, "k3": 2, "comments": "Хорошая работа!"}, f"Ваш результат: 5 из 6 баллов"),
    (ERROR, ERROR)
])
async def test_process_text_input(evaluation_result, expected_message):
    with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post, \
            patch('aiogram.fsm.context.FSMContext.set_state', new_callable=AsyncMock) as mock_set_state, \
            patch('aiogram.fsm.context.FSMContext.update_data', new_callable=AsyncMock) as mock_update_data, \
            patch('aiogram.fsm.context.FSMContext.get_data', new_callable=AsyncMock) as mock_get_data, \
            patch('aiogram.fsm.context.FSMContext.get_state', new_callable=AsyncMock) as mock_get_state:

        handler = MessageHandler(process_text_input, StateFilter(TestStates.waiting_for_text_input))
        requester = MockedBot(handler)

        user_text = "This is a student's email."
        chosen_letter = LETTER_ONE

        mock_get_data.return_value = {"chosen_letter": chosen_letter}
        mock_get_state.return_value = TestStates.waiting_for_text_input

        # мокать будем именно ответ сервера, а не функцию send_to_api
        if evaluation_result == ERROR:
            mock_post.return_value = MockResponse(None, 400)
        else:
            mock_post.return_value = MockResponse(evaluation_result, 200)

        calls = await requester.query(MESSAGE.as_object(text=user_text))

        mock_set_state.assert_called_with(state=None)
        mock_update_data.assert_any_call(user_text=user_text)
        if evaluation_result != ERROR:
            mock_update_data.assert_any_call(result=evaluation_result)

        answer_message = calls.send_message.fetchone()
        assert answer_message.text == expected_message


@pytest.mark.asyncio
async def test_get_comments():
    handler = CallbackQueryHandler(get_comments, F.data == 'get_comments')
    requester = MockedBot(handler)

    with patch('aiogram.fsm.context.FSMContext.get_data',
               return_value={'result': {'k1': 1, 'k2': 2, 'k3': 1, 'comments': 'Good job!'}}):
        calls = await requester.query(
            CALLBACK_QUERY.as_object(data='get_comments', message=MESSAGE.as_object(text="Йоу, бот!")))
        answer_message = calls.send_message.fetchone()
        assert answer_message.text.startswith("Решение коммуникативной задачи:")


@pytest.mark.asyncio
async def test_view_my_work():
    handler = CallbackQueryHandler(view_my_work, F.data == 'view_my_work')
    requester = MockedBot(handler)

    with patch('aiogram.fsm.context.FSMContext.get_data', return_value={'user_text': 'This is my work.'}):
        calls = await requester.query(
            CALLBACK_QUERY.as_object(data='view_my_work', message=MESSAGE.as_object(text="Йоу, бот!")))
        answer_message = calls.send_message.fetchone()
        assert answer_message.text.startswith("Ваша работа:")


@pytest.mark.asyncio
async def test_start_over():
    handler = MessageHandler(start_over, Command("evaluate"))
    requester = MockedBot(handler)
    calls = await requester.query(MESSAGE.as_object(text="/evaluate"))
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == RESTART_MESSAGE
    assert 'email_1' in answer_message.reply_markup['inline_keyboard'][0][0]['callback_data']
    handler = CallbackQueryHandler(start_over, F.data == 'restart')
    requester = MockedBot(handler)
    calls = await requester.query(CALLBACK_QUERY.as_object(data='restart', message=MESSAGE.as_object(text="Йоу, бот!")))
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == RESTART_MESSAGE
    assert 'email_1' in answer_message.reply_markup['inline_keyboard'][0][0]['callback_data']
