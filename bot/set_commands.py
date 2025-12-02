from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllGroupChats, BotCommandScopeAllChatAdministrators, \
    BotCommandScopeAllPrivateChats, BotCommandScopeDefault

async def initialise_commands(bot: Bot):
    commands_gc = [
        BotCommand(command="list", description="Показать белый список"),
        BotCommand(command="add_user", description="@user - Добавить user в белый список"),
    ]
    commands_all = [
        BotCommand(command="start", description="Краткий обзор"),
        BotCommand(command="help", description="Инструкция"),
    ]
    await bot.set_my_commands(
        commands=commands_gc,
        scope=BotCommandScopeAllGroupChats()
    )
    await bot.set_my_commands(
        commands=commands_all,
        scope=BotCommandScopeDefault()
    )
