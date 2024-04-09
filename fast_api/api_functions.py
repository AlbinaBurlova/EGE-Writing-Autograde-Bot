import logging

import httpx

from config_reader import config
from utils.strings import ERROR


async def send_to_api(text, letter):

    url = config.api_address

    data = {
        "data": {
            "Question": letter,
            "Text": text
        }
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return ERROR

    except Exception as e:
        logging.error(f"Error sending to API: {e}")
        return ERROR
