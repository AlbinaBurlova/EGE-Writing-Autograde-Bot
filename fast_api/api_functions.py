import httpx

from utils.strings import ERROR


async def send_to_api(text, letter):

    url = "https://d5d08u0j2sectp2kvlgr.apigw.yandexcloud.net/predict"

    data = {
        "data": {
            "Question": text,
            "Text": letter
        }
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=data)

    if response.status_code == 200:
        return response.json()["k1"]
    else:
        return ERROR
