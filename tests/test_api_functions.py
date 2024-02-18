from unittest.mock import AsyncMock, patch

import pytest
from httpx import Response

from fast_api.api_functions import send_to_api
from utils.strings import ERROR


@pytest.mark.asyncio
async def test_send_to_api():
    text = "text of the task"
    letter = "text of the student's letter"

    mock_response_success = AsyncMock(spec=Response)
    mock_response_success.status_code = 200
    mock_response_success.json.return_value = {"result": "success"}

    mock_response_client_error = AsyncMock(spec=Response)
    mock_response_client_error.status_code = 400

    mock_response_server_error = AsyncMock(spec=Response)
    mock_response_server_error.status_code = 500

    with patch('httpx.AsyncClient.post', return_value=mock_response_success):
        result = await send_to_api(text, letter)
        assert result == {"result": "success"}

    with patch('httpx.AsyncClient.post', return_value=mock_response_client_error):
        result = await send_to_api(text, letter)
        assert result == ERROR

    with patch('httpx.AsyncClient.post', return_value=mock_response_server_error):
        result = await send_to_api(text, letter)
        assert result == ERROR

    with patch('httpx.AsyncClient.post', side_effect=Exception("Test exception")):
        result = await send_to_api(text, letter)
        assert result == ERROR
