import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from config_reader import config
from handlers import (start, evaluate, rate, get_stat, get_secret,
                      help, other_handlers)
from utils.menu import set_main_menu


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    bot = Bot(token=config.bot_token.get_secret_value(),
              parse_mode="HTML")

    dp = Dispatcher()

    dp.include_routers(start.router,
                       evaluate.router,
                       help.router,
                       rate.router,
                       get_stat.router,
                       get_secret.router,
                       other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
