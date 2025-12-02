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
from commands.dispatcher import dp
from commands import public_commands, basic_commands, private_commands
from .set_commands import initialise_commands

async def activate() -> None:
    directory = Path(__file__).resolve().parent.parent / "secrets" / "bot_secret.txt"
    file = open(directory)
    bot_token = file.read().strip()
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await initialise_commands(bot)
    await dp.start_polling(bot)
