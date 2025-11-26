import asyncio
import logging
import sys
from os import getenv
from pathlib import Path
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from commands import basic_commands, admin_commands
from commands.dispatcher import dp

async def activate() -> None:
    directory = Path(__file__).resolve().parent.parent / "secrets" / "bot_secret.txt"
    file = open(directory)
    bot_token = file.read().strip()
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)
