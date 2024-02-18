from unittest.mock import patch, AsyncMock

import pytest
from aiogram import F

from .aiogram_tests import MockedBot
from .aiogram_tests.handler import CallbackQueryHandler
from .aiogram_tests.types.dataset import MESSAGE, CALLBACK_QUERY
from handlers.evaluate import msg_display_letter
from utils.strings import LETTER_TWO


@pytest.mark.asyncio
async def test_msg_display_letter():
    handler = CallbackQueryHandler(msg_display_letter, F.data.startswith('email'))
    requester = MockedBot(handler)
    with patch('aiogram.fsm.context.FSMContext.update_data', new_callable=AsyncMock) as mock_update_data:
        await requester.query(CALLBACK_QUERY.as_object(data='email_2', message=MESSAGE.as_object(text="Йоу, бот!")))
        mock_update_data.assert_called_once_with(chosen_letter=LETTER_TWO)
