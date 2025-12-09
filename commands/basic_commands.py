from aiogram import html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from .dispatcher import basic_router


@basic_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # if message.chat.id < 0: - проверка на групповой чат
    # await ensure_chat_in_db - добавили в чат пока спал => добавляем в бд
    await message.answer("Привет! Я - Бот-Кондуктор, здесь, "
                         "чтобы контролировать белый список!\n"
                         "Чтобы узнать, как мной пользоваться, напиши /help.")


@basic_router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    # if message.chat.id < 0:
    # await ensure_chat_in_db
    await message.answer(f"{html.bold("Инструкция:")}\n"
                         f"{html.bold("Общие функции:")}\n"
                         "/start - приветствие\n"
                         "/help - инструкция\n"
                         "/list - белый список\n"
                         f"{html.bold("Функции для админов:")}\n"
                         "/add_user @user - добавить user в белый список\n"
                         "/remove_user @user - удалить user из списка\n"
                         "/pause - поставить контроль списка на паузу\n"
                         "/unpause - убрать контроль списка с паузы\n"
                         "/add_all_members - добавить всех членов чата "
                         "в список\n"
                         "/remove_all_members - очистить белый список "
                         "(опасно!)\n"
                         f"{html.bold("Важно!")} "
                         "Чтобы я мог выполнять свою работу, необходимо "
                         "выдать мне админское право на кик людей. "
                         "Админов и себя я не кикаю.")
