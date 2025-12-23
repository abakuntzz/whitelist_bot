import pytest
from unittest.mock import AsyncMock, Mock


@pytest.fixture
def mock_message() -> AsyncMock:
    """Мок сообщения в чате"""
    message = AsyncMock()
    message.chat.id = -1001234567890
    message.from_user.id = 123456789
    message.answer = AsyncMock()
    return message


@pytest.fixture
def mock_message_admin() -> AsyncMock:
    """Мок сообщения от админа"""
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
def mock_message_user() -> AsyncMock:
    """Мок сообщения от не админа"""
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
def mock_command() -> AsyncMock:
    """Мок команды телеграм"""
    command = AsyncMock()
    command.args = None
    return command


@pytest.fixture
def mock_db_session() -> AsyncMock:
    """Мок сессии базы данных"""
    session = AsyncMock()

    mock_result = Mock()
    mock_result.scalar_one_or_none = Mock(return_value=None)
    mock_result.fetchall = Mock(return_value=[])
    mock_result.rowcount = 0

    session.execute = AsyncMock(return_value=mock_result)
    session.add = AsyncMock()
    session.commit = AsyncMock()

    return session


@pytest.fixture
def mock_bot() -> AsyncMock:
    """Мок бота"""
    bot = AsyncMock()
    bot.set_my_commands = AsyncMock()
    return bot


@pytest.fixture
def mock_telethon_helper() -> AsyncMock:
    """Мок TelethonHelper"""
    helper = AsyncMock()
    helper.initialize = AsyncMock()
    helper.shutdown = AsyncMock()
    helper.master_check = AsyncMock()
    helper.get_chat_members = AsyncMock()
    helper.kick_user = AsyncMock()
    helper.get_user_by_username = AsyncMock()
    helper.get_user_by_id = AsyncMock()
    helper.chat_check = AsyncMock()
    return helper


@pytest.fixture
def mock_telegram_client() -> AsyncMock:
    """Мок TelegramClient"""
    client = AsyncMock()
    client.start = AsyncMock()
    client.get_me = AsyncMock()
    client.disconnect = AsyncMock()
    client.iter_participants = AsyncMock()
    client.get_entity = AsyncMock()
    client.kick_participant = AsyncMock()
    client.get_permissions = AsyncMock()
    return client
