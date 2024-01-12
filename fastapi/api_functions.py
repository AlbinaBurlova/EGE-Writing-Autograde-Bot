import httpx

from utils.strings import ERROR


async def send_to_api(text, letter):

    url = "http://localhost:8000/predict"

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
