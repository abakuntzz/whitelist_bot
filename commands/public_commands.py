import asyncio
import logging
import sys
from os import getenv
from pathlib import Path
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject, ChatMemberUpdatedFilter,\
    IS_NOT_MEMBER, IS_MEMBER, IS_ADMIN
from aiogram.types import Message, ChatMemberUpdated
from .dispatcher import dp, public_router

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
    # users = get_chat_whitelist(message.chat.id) *должен возвращать список userId
    await message.answer(output)


@public_router.message(Command("add_user"))
@admin_required
async def command_add_user_handler(message: Message, command: CommandObject) -> None:
    commands = command.args
    if commands is None:
        await message.answer("Вы не передали параметр. Использование: /add_user @user")
        return
    username = commands.split()[0]
    try:
        user = await dp['telethon_helper'].get_user_by_username(username)
        # await add_user_to_whitelist(message.chat.id, user['id'])
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
        user = await dp['telethon_helper'].get_user_by_username(username)
        # done = await remove_user_from_whitelist(message.chat.id, user['id']) *true - такой был, false - такого не было
        # if not done: await message.answer(f"Пользователь не найден в белом списке")
        # else:
        # if not get_pause_status(message.chat.id): 
        try:
            await dp['telethon_helper'].kick_user(message.chat.id, user['id'])
        except Exception:
            pass
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
        await dp['telethon_helper'].chat_check(message.chat.id)
        await message.answer("Контроль белого списка активирован.")
    except Exception as e:
        await message.answer(f"Не удалось убрать с паузы: {e}")


@public_router.message(Command("add_all_members"))
@admin_required
async def command_add_all_members_handler(message: Message, command: CommandObject) -> None:
    try:
        chat_id = message.chat.id
        # users = await dp['telethon_helper'].get_chat_members(chat_id)
        # for user in users:
        #     await add_user_to_whitelist(chat_id, user['id'])
        await message.answer("Все пользователи добавлены в белый список.")
    except Exception as e:
        await message.answer(f"Не удалось добавить всех: {e}")


@public_router.message(Command("remove_all_members"))
@admin_required
async def command_remove_all_members_handler(message: Message, command: CommandObject) -> None:
    try:
        # await clear_whitelist(message.chat.id)
        # await dp['telethon_helper'].chat_check(message.chat.id)
        await message.answer("Белый список успешно очищен.")
    except Exception as e:
        await message.answer(f"Не удалось очистить белый список: {e}")


# для отладки
@public_router.message(Command("list_all"))
@admin_required
async def command_list_all_handler(message: Message, command: CommandObject) -> None:
    try:
        telethon_helper = dp['telethon_helper']
        if not telethon_helper:
            from .telethon_helper import TelethonHelper
            telethon_helper = TelethonHelper()
        members = await telethon_helper.get_chat_members(message.chat.id)      
        if not members:
            await message.answer("Не найдено пользователей в чате")
            return  
        response = f"👥 Участники чата ({len(members)}):\n\n"
        for i, member in enumerate(members[:50], 1):
            username = f"@{member['username']}" if member['username'] else "без username"
            if member['is_admin'] == 2:
                status = "👑 "
            elif member['is_admin'] == 1:
                status = "👮 "
            else:
                status = ""
            last_name = f" {member['last_name']}" if member['last_name'] else ""
            response += f"{i}. {status}{member['first_name']}{last_name} ({username})\n"
        if len(members) > 50:
            response += f"\n... и ещё {len(members) - 50} участников"
        await message.answer(response)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {type(e).__name__}: {str(e)}")


@public_router.my_chat_member(
    ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def bot_added_to_chat(event: ChatMemberUpdated):
    print(f"[!] Меня добавили в чат: {event.chat.id}")
    # await add_chat_to_database(event.chat.id)


@public_router.chat_member(
    ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def handle_new_chat_member(event: ChatMemberUpdated):
    user_id = event.new_chat_member.user.id
    print(f"[!] Новый участник чата: {user_id}")
    okay = True # потом убрать
    # okay = await find_id_in_whitelist(event.chat.id, user_id')
    # if not get_pause_status(message.chat.id):
    if not okay: 
        try:
            await dp['telethon_helper'].kick_user(event.chat.id, user_id)
        except Exception:
            pass
