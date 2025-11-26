import asyncio
import logging
import sys
from os import getenv
from pathlib import Path
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from .dispatcher import basic_router

@basic_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!")

@basic_router.message(Command("help"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Инструкция: ...")
