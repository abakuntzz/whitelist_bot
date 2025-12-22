import pytest
from unittest.mock import patch, AsyncMock, Mock, MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import commands.telethon_helper as telethon_helper


@pytest.mark.asyncio
async def test_singleton_pattern():
    helper1 = telethon_helper.TelethonHelper()
    helper2 = telethon_helper.TelethonHelper()
    assert helper1 is helper2
    assert id(helper1) == id(helper2)


@pytest.mark.asyncio
async def test_initialize(mock_telegram_client):
    helper = telethon_helper.TelethonHelper()
    mock_me = Mock(id=123456789)
    mock_telegram_client.get_me = AsyncMock(return_value=mock_me)
    
    with patch.object(telethon_helper, 'TelegramClient', return_value=mock_telegram_client):
        await helper.initialize(12345, "test_api_hash", "test_bot_token")
        assert helper._initialized is True
        assert helper._me.id == 123456789
        mock_telegram_client.start.assert_called_once_with(bot_token="test_bot_token")
        mock_telegram_client.get_me.assert_called_once()


@pytest.mark.asyncio
async def test_shutdown(mock_telegram_client):
    helper = telethon_helper.TelethonHelper()
    mock_telegram_client.disconnect = AsyncMock()
    helper._client = mock_telegram_client
    helper._initialized = True
    await helper.shutdown()
    mock_telegram_client.disconnect.assert_called_once()
    assert helper._client is None
    assert helper._initialized is False


@pytest.mark.asyncio
async def test_kick_user_other(mock_telegram_client):
    helper = telethon_helper.TelethonHelper()
    helper._me = Mock(id=123456789)
    helper._client = mock_telegram_client
    mock_user = Mock()
    mock_telegram_client.get_entity = AsyncMock(return_value=mock_user)
    mock_telegram_client.kick_participant = AsyncMock()
    result = await helper.kick_user(-1001234567890, 987654321)
    assert result is True
    mock_telegram_client.get_entity.assert_called_once_with(987654321)
    mock_telegram_client.kick_participant.assert_called_once_with(-1001234567890, mock_user)


@pytest.mark.asyncio
async def test_kick_user_self(mock_telegram_client):
    helper = telethon_helper.TelethonHelper()
    helper._me = Mock(id=123456789)
    helper._client = mock_telegram_client
    result = await helper.kick_user(-1001234567890, 123456789)
    assert result is False
    mock_telegram_client.get_entity.assert_not_called()
    mock_telegram_client.kick_participant.assert_not_called()


@pytest.mark.asyncio
async def test_get_chat_members_empty():
    helper = telethon_helper.TelethonHelper()
    
    async def empty_iter_participants(chat_id):
        if False:
            yield
    
    helper._client = AsyncMock()
    helper._client.iter_participants = empty_iter_participants
    
    result = await helper.get_chat_members(-1001234567890)
    assert result == []


@pytest.mark.asyncio
async def test_get_user_by_username():
    helper = telethon_helper.TelethonHelper()
    helper._client = AsyncMock()
    mock_user = Mock(id=123456789, username="testuser", first_name="Тест", 
                     last_name="Пользователь", bot=False)
    helper._client.get_entity = AsyncMock(return_value=mock_user)
    result = await helper.get_user_by_username("@testuser")
    helper._client.get_entity.assert_called_once_with("testuser")
    assert result is not None
    assert result['id'] == 123456789
    assert result['username'] == "testuser"
    assert result['first_name'] == "Тест"
    assert result['last_name'] == "Пользователь"
    assert result['is_bot'] is False


@pytest.mark.asyncio
async def test_get_user_by_id():
    helper = telethon_helper.TelethonHelper()
    helper._client = AsyncMock()
    mock_user = Mock(id=123456789, username="testuser", first_name="Тест", 
                     last_name="Юзер", bot=True)
    helper._client.get_entity = AsyncMock(return_value=mock_user)
    result = await helper.get_user_by_id(123456789)
    assert result is not None
    assert result['id'] == 123456789
    assert result['username'] == "testuser"
    assert result['first_name'] == "Тест"
    assert result['last_name'] == "Юзер"
    assert result['is_bot'] is True


@pytest.mark.asyncio
async def test_chat_check():
    helper = telethon_helper.TelethonHelper()
    mock_members = [
        {'id': 111, 'username': 'user1'},
        {'id': 222, 'username': 'user2'},
        {'id': 333, 'username': 'user3'}
    ]
    helper.get_chat_members = AsyncMock(return_value=mock_members)
    helper.kick_user = AsyncMock(return_value=True)
    
    side_effect = [True, False, True]
    with patch.object(telethon_helper, 'is_user_in_whitelist', AsyncMock(side_effect=side_effect)):
        result = await helper.chat_check(-1001234567890)
        assert result is True
        assert helper.kick_user.call_count == 1
        helper.kick_user.assert_called_once_with(-1001234567890, 222)
