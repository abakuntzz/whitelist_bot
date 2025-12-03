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
from commands.telethon_helper import TelethonHelper
from commands.dispatcher import dp
from commands import public_commands, basic_commands, private_commands
from .set_commands import initialise_commands

async def activate() -> None:
    try:
        directory = Path(__file__).resolve().parent.parent / "secrets" 
        with open(directory / "bot_secret.txt") as f:
            bot_token = f.read().strip()
        with open(directory / "api_id.txt") as f:
            api_id = f.read().strip()
        with open(directory / "api_hash.txt") as f:
            api_hash = f.read().strip()
        telethon_helper = TelethonHelper()
        await telethon_helper.initialize(api_id, api_hash, bot_token)
        bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp['telethon_helper'] = telethon_helper
        await initialise_commands(bot)
        await dp.start_polling(bot)
    finally:
        try:
            await dp['telethon_helper'].shutdown()
        except Exception:
            pass
