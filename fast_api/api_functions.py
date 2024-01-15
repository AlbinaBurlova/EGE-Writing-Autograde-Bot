import httpx

from utils.strings import ERROR, WAIT_FOR_TOO_LONG

async def send_to_api(text, letter):

    url = "https://d5d08u0j2sectp2kvlgr.apigw.yandexcloud.net/predict"

    data = {
        "data": {
            "Question": text,
            "Text": letter
        }
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return ERROR
    except (httpx.ConnectTimeout, httpx.ReadTimeout):
        return WAIT_FOR_TOO_LONG
