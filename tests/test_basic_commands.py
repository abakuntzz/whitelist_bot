import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import commands.basic_commands as basic_commands

START_EXPECTED = (
    "Привет! Я - Бот-Кондуктор, здесь, "
    "чтобы контролировать белый список!\n"
    "Чтобы узнать, как мной пользоваться, напиши /help."
)

HELP_EXPEXTED = (
    "<b>Инструкция:</b>\n"
    "<b>Общие функции:</b>\n"
    "/start - приветствие\n"
    "/help - инструкция\n"
    "/list - белый список\n"
    "<b>Функции для админов:</b>\n"
    "/add_user @user - добавить user в белый список\n"
    "/remove_user @user - удалить user из списка\n"
    "/pause - поставить контроль списка на паузу\n"
    "/unpause - убрать контроль списка с паузы\n"
    "/add_all_members - добавить всех членов чата в список\n"
    "/remove_all_members - очистить белый список (опасно!)\n"
    "<b>Важно!</b> "
    "Чтобы я мог выполнять свою работу, необходимо "
    "выдать мне админское право на кик людей. "
    "Админов и себя я не кикаю."
)


@pytest.mark.asyncio
async def test_command_start_handler(mock_message) -> None:

    await basic_commands.command_start_handler(mock_message)

    mock_message.answer.assert_called_once()
    response_text = mock_message.answer.call_args[0][0]
    
    assert response_text == START_EXPECTED


@pytest.mark.asyncio
async def test_command_help_handler(mock_message) -> None:

    await basic_commands.command_help_handler(mock_message)
    
    mock_message.answer.assert_called_once()
    response_text = mock_message.answer.call_args[0][0]
    
    assert response_text == HELP_EXPEXTED 
