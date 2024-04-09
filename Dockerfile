FROM python:3.9-slim-bullseye

WORKDIR /bot
COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD [ "python", "bot.py" ]
