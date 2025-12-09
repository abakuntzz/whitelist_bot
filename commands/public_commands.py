import logging
from aiogram import html
from aiogram.filters import Command, CommandObject, ChatMemberUpdatedFilter, \
    IS_NOT_MEMBER, IS_MEMBER, IS_ADMIN
from aiogram.types import Message, ChatMemberUpdated
from .dispatcher import dp, public_router
from database.commands import update_pause_status, get_chat_status, \
    add_user_to_whitelist, remove_user_from_whitelist, get_whitelist_by_chat, \
    is_user_in_whitelist
from functools import wraps
from aiogram.methods import GetChatAdministrators


def admin_required(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        admins = await message.bot(GetChatAdministrators
                                   (chat_id=message.chat.id))
        user_is_admin = any(admin.user.id == message.from_user.id
                            for admin in admins)
        if not user_is_admin:
            await message.answer("Эта команда только для админов чата!")
            return
        return await func(message, *args, **kwargs)
    return wrapper


@public_router.message(Command("list"))
async def command_list_handler(message: Message) -> None:
    output = f"{html.bold("Белый список:")}\n"
    chat_id = message.chat.id
    users = await get_whitelist_by_chat(chat_id)
    if not users:
        output += "Пусто...\n"
    else:
        i = 0
        for id in users:
            i += 1
            name = await dp['telethon_helper'].get_user_by_id(int(id))
            if name:
                output += f"{i}. {name['first_name']} {name['last_name']} " + \
                          f"({name['username']})\n"
    paused = await get_chat_status(chat_id)
    output += f"{html.bold("Статус:")} "
    output += "OFF.\n" if paused else "ON.\n"
    await message.answer(output)


@public_router.message(Command("add_user"))
@admin_required
async def command_add_user_handler(message: Message,
                                   command: CommandObject) -> None:
    commands = command.args
    if commands is None:
        await message.answer("Вы не передали параметр. Использование: "
                             "/add_user @user")
        return
    username = commands.split()[0]
    chat_id = message.chat.id
    try:
        user = await dp['telethon_helper'].get_user_by_username(username)
        done = await add_user_to_whitelist(chat_id, user['id'])
        if not done[0]:
            await message.answer(f"Не удалось добавить пользователя: "
                                 f"{done[1]}.")
        else:
            await message.answer(f"Пользователь {username} "
                                 "добавлен в белый список.")
    except Exception as e:
        logging.info(f"Не удалось обработать add_user {username} "
                     f"в чате {chat_id} - {e}")
        await message.answer(f"Не удалось добавить {username} "
                             "в белый список.")


@public_router.message(Command("remove_user"))
@admin_required
async def command_remove_user_handler(message: Message,
                                      command: CommandObject) -> None:
    commands = command.args
    if commands is None:
        await message.answer("Вы не передали параметр. Использование: "
                             "/remove_user @user")
        return
    username = commands.split()[0]
    chat_id = message.chat.id
    user = await dp['telethon_helper'].get_user_by_username(username)
    done = await remove_user_from_whitelist(chat_id, user['id'])
    if not done:
        await message.answer("Пользователь не найден в белом списке")
    else:
        pause = await get_chat_status(chat_id)
        if not pause:
            await dp['telethon_helper'].kick_user(message.chat.id, user['id'])
        await message.answer(f"Пользователь {username} "
                             "удалён из белого списка.")


@public_router.message(Command("pause"))
@admin_required
async def command_pause_handler(message: Message,
                                command: CommandObject) -> None:
    done = await update_pause_status(message.chat.id, True)
    if done:
        await message.answer("Контроль белого списка на паузе. Чтобы вновь "
                             "его активировать, напишите /unpause.")
    else:
        await message.answer("Не удалось поставить на паузу.")


@public_router.message(Command("unpause"))
@admin_required
async def command_unpause_handler(message: Message,
                                  command: CommandObject) -> None:
    chat_id = message.chat.id
    await update_pause_status(chat_id, False)
    await dp['telethon_helper'].chat_check(chat_id)
    await message.answer("Контроль белого списка активирован.")


@public_router.message(Command("add_all_members"))
@admin_required
async def command_add_all_members_handler(message: Message,
                                          command: CommandObject) -> None:
    chat_id = message.chat.id
    users = await dp['telethon_helper'].get_chat_members(chat_id)
    for user in users:
        await add_user_to_whitelist(chat_id, user['id'])
    await message.answer("Все пользователи добавлены в белый список.")


@public_router.message(Command("remove_all_members"))
@admin_required
async def command_remove_all_members_handler(message: Message,
                                             command: CommandObject) -> None:
    chat_id = message.chat.id
    users = await get_whitelist_by_chat(chat_id)
    for user in users:
        await remove_user_from_whitelist(chat_id, user)
    pause = await get_chat_status(chat_id)
    if not pause:
        await dp['telethon_helper'].chat_check(chat_id)
    await message.answer("Белый список успешно очищен.")


@public_router.my_chat_member(
    ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def bot_added_to_chat(event: ChatMemberUpdated):
    chat_id = event.chat.id
    logging.info(f"Меня добавили в чат: {chat_id}")
    # await add_chat_to_database(chat_id) ВАЖНО: даже если чат уже есть,
    # в нём ставим паузу!!


@public_router.chat_member(
    ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def handle_new_chat_member(event: ChatMemberUpdated):
    user_id = event.new_chat_member.user.id
    chat_id = event.chat.id
    pause = await get_chat_status(chat_id)
    if not pause:
        okay = await is_user_in_whitelist(chat_id, user_id)
        if not okay:
            done = await dp['telethon_helper'].kick_user(chat_id, user_id)
            if done:
                await event.answer("Новый пользователь удалён: "
                                   "нет в белом списке.")


@public_router.chat_member(
    ChatMemberUpdatedFilter(IS_ADMIN >> IS_MEMBER)
)
async def handle_unadmin(event: ChatMemberUpdated):
    user_id = event.new_chat_member.user.id
    chat_id = event.chat.id
    pause = await get_chat_status(chat_id)
    if not pause:
        okay = await is_user_in_whitelist(chat_id, user_id)
        if not okay:
            await dp['telethon_helper'].kick_user(chat_id, user_id)
