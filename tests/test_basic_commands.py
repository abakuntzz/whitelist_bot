import pytest
from unittest.mock import patch, AsyncMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import commands.basic_commands as basic_commands
@pytest.mark.asyncio
async def test_command_start_handler(mock_message):
    """Тест команды /start"""
    await basic_commands.command_start_handler(mock_message)
    
    mock_message.answer.assert_called_once()
    
    response_text = mock_message.answer.call_args[0][0]
    assert "Привет" in response_text
    assert "Бот-Кондуктор" in response_text
    assert "/help" in response_text

@pytest.mark.asyncio
async def test_command_help_handler(mock_message):
    """Тест команды /help"""
    await basic_commands.command_help_handler(mock_message)
    
    mock_message.answer.assert_called_once()
    
    response_text = mock_message.answer.call_args[0][0]
    assert "Инструкция" in response_text
    assert "/start" in response_text
    assert "/list" in response_text
    assert "админов" in response_text
