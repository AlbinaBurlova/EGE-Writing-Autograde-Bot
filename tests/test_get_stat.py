import os
from unittest.mock import patch

import matplotlib.pyplot as plt
import pytest
from aiogram import F
from aiogram import types
from aiogram.filters import Command

from .aiogram_tests import MockedBot
from .aiogram_tests.handler import MessageHandler, CallbackQueryHandler
from .aiogram_tests.types.dataset import MESSAGE, CALLBACK_QUERY
from handlers import get_stat
from handlers.get_stat import show_stat, calculate_averages, create_plot


async def run_test(handler, event):
    with patch('handlers.get_stat.calculate_averages', return_value={'score': 4.5}), \
            patch('handlers.get_stat.create_plot', return_value='plot.png'), \
            patch('os.remove') as mock_remove:

        # Сначала проверьте сценарий, когда результатов нет
        get_stat.results.clear()
        requester = MockedBot(handler)
        calls = await requester.query(event)
        request = requester.get_last_request()
        if isinstance(request, types.Message):
            assert request.reply_markup is None
        if isinstance(handler, MessageHandler):
            answer_message = calls.send_message.fetchone()
        else:
            answer_message = calls.answer_callback_query.fetchone()
        assert answer_message.text == "Для статистики пока не хватает данных."

        # Затем проверьте сценарий, когда результаты есть
        get_stat.results.append({'score': 5, 'comments': 'Great!'})
        calls = await requester.query(event)
        request = requester.get_last_request()
        assert hasattr(request, 'photo')
        assert isinstance(request.photo, types.InputFile)
        mock_remove.assert_called_once_with('plot.png')
        if isinstance(handler, MessageHandler):
            answer_message = calls.send_message.fetchone()
        else:
            answer_message = calls.answer_callback_query.fetchone()
        assert answer_message.text.startswith("Средние результаты оценки:")


@pytest.mark.asyncio
async def test_show_stat_message():
    mock_message = MESSAGE.as_object(text="/get_stat")
    await run_test(MessageHandler(show_stat, Command("get_stat")), mock_message)


@pytest.mark.asyncio
async def test_show_stat_callback():
    mock_message = MESSAGE.as_object(text="/get_stat")
    mock_callback = CALLBACK_QUERY.as_object(message=mock_message, data='get_stat')
    await run_test(CallbackQueryHandler(show_stat, F.data == "get_stat"), mock_callback)


def test_calculate_averages():
    results = [{'a': 1, 'b': 2, 'comments': 'Great!'}, {'a': 3, 'b': 4, 'comments': 'Good job!'}]
    averages = calculate_averages(results)
    assert averages == {'a': 2, 'b': 3}


def test_create_plot():
    averages = {'a': 2, 'b': 3}
    plot_file = create_plot(averages)
    assert plt.gcf() is not None
    plt.close()
    os.remove(plot_file)
