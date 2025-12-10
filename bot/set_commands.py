from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllGroupChats, \
    BotCommandScopeDefault


async def initialise_commands(bot: Bot) -> None:
    commands_gc = [
        BotCommand(command="list",
                   description="Показать белый список"),
        BotCommand(command="add_user",
                   description="@user - Добавить user в белый список"),
        BotCommand(command="remove_user",
                   description="@user - Удалить user из списка"),
        BotCommand(command="pause",
                   description="Поставить контроль списка на паузу"),
        BotCommand(command="unpause",
                   description="Убрать контроль списка с паузы"),
        BotCommand(command="add_all_members",
                   description="Добавить всех членов чата в список"),
        BotCommand(command="remove_all_members",
                   description="Очистить белый список")
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
