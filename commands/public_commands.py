import asyncio
import logging
import sys
from os import getenv
from pathlib import Path
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from .dispatcher import public_router

from functools import wraps
from aiogram.types import Message
from aiogram.methods import GetChatAdministrators, GetChatMember
from aiogram.types import ChatMemberOwner, ChatMemberAdministrator


def admin_required(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        admins = await message.bot(GetChatAdministrators(chat_id=message.chat.id))
        user_is_admin = any(admin.user.id == message.from_user.id for admin in admins)
        if not user_is_admin:
            await message.answer("Эта команда только для администраторов чата!")
            return
        return await func(message, *args, **kwargs)
    return wrapper


@public_router.message(Command("list"))
async def command_list_handler(message: Message) -> None:
    output = "Белый список: "
    # get_chat_whitelist
    await message.answer(output)


# вместо userId в БД надо сделать username!!! (заранее перевести в маленькие буквы)
@public_router.message(Command("add_user"))
@admin_required
async def command_add_user_handler(message: Message, command: CommandObject) -> None:
    commands = command.args
    if commands is None:
        await message.answer("Вы не передали параметр. Использование: /add_user @user")
        return
    username = commands.split()[0]
    if username[0] != "@":
        await message.answer("Некорректно введён параметр. Использование: /add_user @user")
        return
    try:
        # await add_user_to_whitelist(username[1:], message.chat.id)
        await message.answer(f"Пользователь {username} добавлен в белый список.")
    except Exception as e:
        await message.answer(f"Не удалось добавить пользователя: {e}")


@public_router.message(Command("remove_user"))
@admin_required
async def command_remove_user_handler(message: Message, command: CommandObject) -> None:
    commands = command.args
    if commands is None:
        await message.answer("Вы не передали параметр. Использование: /remove_user @user")
        return
    username = commands.split()[0]
    if username[0] != "@":
        await message.answer("Некорректно введён параметр. Использование: /remove_user @user")
        return
    try:
        # await remove_user_from_whitelist(username[1:], message.chat.id)
        # await check_for_kick(username[1:], message.chat.id)
        await message.answer(f"Пользователь {username} удалён из белого списка.")
    except Exception as e:
        await message.answer(f"Не удалось удалить пользователя: {e}")


@public_router.message(Command("pause"))
@admin_required
async def command_pause_handler(message: Message, command: CommandObject) -> None:
    try:
        # await pause(message.chat.id)
        await message.answer("Контроль белого списка на паузе. Чтобы вновь его активировать, напишите /unpause.")
    except Exception as e:
        await message.answer(f"Не удалось поставить на паузу: {e}")


@public_router.message(Command("unpause"))
@admin_required
async def command_unpause_handler(message: Message, command: CommandObject) -> None:
    try:
        # await unpause(message.chat.id)
        await message.answer("Контроль белого списка активирован.")
    except Exception as e:
        await message.answer(f"Не удалось убрать с паузы: {e}")


@public_router.message(Command("remove_all_members"))
@admin_required
async def command_remove_all_members_handler(message: Message, command: CommandObject) -> None:
    try:
        # await clear_whitelist(message.chat.id)
        await message.answer("Белый список успешно очищен.")
    except Exception as e:
        await message.answer(f"Не удалось очистить белый список: {e}")


# add_all_members не получится из соображений приватности :(

