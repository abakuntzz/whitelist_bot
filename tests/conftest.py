import pytest
import asyncio
from unittest.mock import AsyncMock, Mock

@pytest.fixture
def mock_message():
    """Мок сообщения в групповом чате"""
    message = AsyncMock()
    message.chat.id = -1001234567890 
    message.from_user.id = 123456789   
    message.answer = AsyncMock()
    return message


@pytest.fixture
def mock_message_admin():
    """Мок сообщения от администратора чата"""
    message = AsyncMock()
    message.chat.id = -1001234567890
    message.from_user.id = 123456789
    message.answer = AsyncMock()
    
    mock_bot = AsyncMock()
    mock_admin = Mock()
    mock_admin.user = Mock()
    mock_admin.user.id = 123456789  
    mock_bot.return_value = [mock_admin]
    message.bot = mock_bot
    
    return message


@pytest.fixture
def mock_message_user():
    """Мок сообщения от обычного пользователя (не админа)"""
    message = AsyncMock()
    message.chat.id = -1001234567890
    message.from_user.id = 123456789
    message.answer = AsyncMock()
    
    mock_bot = AsyncMock()
    mock_admin = Mock()
    mock_admin.user = Mock()
    mock_admin.user.id = 999999999  
    mock_bot.return_value = [mock_admin]
    message.bot = mock_bot
    
    return message


@pytest.fixture
def mock_command():
    """Мок команды телеграм"""
    command = AsyncMock()
    command.args = None
    return command


@pytest.fixture
def mock_db_session():
    """Мок сессии базы данных"""
    session = AsyncMock()
    mock_result = AsyncMock()

    mock_result.scalar_one_or_none = AsyncMock(return_value=None)
    mock_result.fetchall = Mock(return_value=[])
    mock_result.rowcount = 0
    
    session.execute = AsyncMock(return_value=mock_result)
    session.add = AsyncMock()
    session.commit = AsyncMock()
    
    return session
