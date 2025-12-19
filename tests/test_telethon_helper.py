import pytest
from unittest.mock import patch, AsyncMock, Mock
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
async def test_initialize():
    helper = telethon_helper.TelethonHelper()
    
    mock_client = AsyncMock()
    mock_client.start = AsyncMock()
    mock_client.get_me = AsyncMock(return_value=Mock(id=123456789))
    
    with patch.object(telethon_helper, 'TelegramClient', return_value=mock_client):
        await helper.initialize(
            api_id=12345,
            api_hash="test_api_hash",
            bot_token="test_bot_token"
        )
        
        assert helper._initialized is True
        assert helper._me.id == 123456789
        
        mock_client.start.assert_called_once_with(bot_token="test_bot_token")
        mock_client.get_me.assert_called_once()


@pytest.mark.asyncio
async def test_shutdown():
    helper = telethon_helper.TelethonHelper()
    mock_client = AsyncMock()
    mock_client.disconnect = AsyncMock()
    helper._client = mock_client
    helper._initialized = True
    
    await helper.shutdown()
    
    mock_client.disconnect.assert_called_once()
    
    assert helper._client is None
    assert helper._initialized is False


@pytest.mark.asyncio
async def test_kick_user_other():
    helper = telethon_helper.TelethonHelper()
    helper._me = Mock(id=123456789)
    helper._client = AsyncMock()
    
    mock_user = Mock()
    helper._client.get_entity = AsyncMock(return_value=mock_user)
    helper._client.kick_participant = AsyncMock()
    
    result = await helper.kick_user(
        chat_id=-1001234567890,
        user_id=987654321
    )
    
    assert result == True
    helper._client.get_entity.assert_called_once_with(987654321)
    helper._client.kick_participant.assert_called_once()


@pytest.mark.asyncio
async def test_kick_user_self():
    helper = telethon_helper.TelethonHelper()
    helper._me = Mock(id=123456789)
    helper._client = AsyncMock()
    
    result = await helper.kick_user(
        chat_id=-1001234567890,
        user_id=123456789
    )
    
    assert result == False
    helper._client.get_entity.assert_not_called()
    helper._client.kick_participant.assert_not_called()


@pytest.mark.asyncio
async def test_get_user_by_username():
    helper = telethon_helper.TelethonHelper()
    helper._client = AsyncMock()
    helper._initialized = True
    
    mock_user = Mock()
    mock_user.id = 123456789
    mock_user.username = "testuser"
    mock_user.first_name = "Тест"
    mock_user.last_name = "Пользователь"
    mock_user.bot = False
    
    helper._client.get_entity = AsyncMock(return_value=mock_user)
    
    result = await helper.get_user_by_username("@testuser")
    
    helper._client.get_entity.assert_called_once_with("testuser")
    
    assert result['id'] == 123456789
    assert result['username'] == "testuser"
    assert result['first_name'] == "Тест"
    assert result['last_name'] == "Пользователь"
    assert result['is_bot'] is False


@pytest.mark.asyncio
async def test_chat_check_all_allowed():
    helper = telethon_helper.TelethonHelper()
    
    mock_members = [
        {'id': 111, 'username': 'user1'},
        {'id': 222, 'username': 'user2'},
        {'id': 333, 'username': 'user3'}
    ]
    
    helper.get_chat_members = AsyncMock(return_value=mock_members)
    helper.kick_user = AsyncMock(return_value=True)
    
    with patch.object(telethon_helper, 'is_user_in_whitelist', AsyncMock(return_value=True)):
        result = await helper.chat_check(chat_id=-1001234567890)
        
        assert result is True
        assert helper.kick_user.call_count == 0


@pytest.mark.asyncio
async def test_chat_check_some_kicked():
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
        result = await helper.chat_check(chat_id=-1001234567890)
        
        assert result is True
        assert helper.kick_user.call_count == 1
        helper.kick_user.assert_called_once_with(-1001234567890, 222)
