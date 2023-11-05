import asyncio
import logging
import os
import sys
from core.handler.start import dbc
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
from core.handler.start import router
from aiogram.types import BotCommand


load_dotenv('.env')
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main() -> None:
    bot = Bot(os.getenv('TOKEN'), parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(router)
    commands = [
        BotCommand(command='start', description='Нажмите start чтобы перейти на главную страниццу'),
        # BotCommand()
    ]

    await dbc.connect()
    await bot.set_my_commands(commands=commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
