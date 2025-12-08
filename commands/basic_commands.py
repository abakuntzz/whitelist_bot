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
    # if message.chat.id < 0: - проверка на групповой чат
    # await ensure_chat_in_db - если его добавили в чат пока он спал, добавляем в бд
    await message.answer("Привет! Я - Бот-Кондуктор, здесь, чтобы контролировать белый список!\n"
                         "Чтобы узнать, как мной пользоваться, напиши /help.")

@basic_router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    # if message.chat.id < 0:
    # await ensure_chat_in_db
    await message.answer(f"{html.bold("Инструкция:")}\n"
                         f"{html.bold("Общие функции:")}\n"r"\start - приветствие""\n"r"\help - инструкция""\n"r"\list - белый список""\n"
                         f"{html.bold("Функции для админов:")}\n"
                         f"{html.bold("Важно!")} Чтобы я мог выполнять свою работу, "
                         "необходимо выдать мне админское право на кик людей. Админов и себя я не кикаю.")
