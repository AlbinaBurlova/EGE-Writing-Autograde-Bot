import httpx

from utils.strings import ERROR


async def send_to_api(text, letter):

    url = "https://stunning-star-octopus.ngrok-free.app/predict"

    data = {
        "data": {
            "Question": letter,
            "Text": text
        }
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return ERROR
