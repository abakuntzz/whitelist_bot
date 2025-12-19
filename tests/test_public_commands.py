import pytest
from unittest.mock import patch, AsyncMock, Mock, call
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import commands.public_commands as public_commands


@pytest.mark.asyncio
async def test_command_pause_handler():
    message = AsyncMock()
    message.chat.id = -1001234567890
    message.from_user.id = 123456789
    message.answer = AsyncMock()
    
    mock_admin = Mock()
    mock_admin.user = Mock()
    mock_admin.user.id = 123456789
    message.bot = AsyncMock(return_value=[mock_admin])
    
    command = AsyncMock()
    command.args = None
    
    mock_update_pause_status = AsyncMock(return_value=True)
    
    with patch.object(public_commands, 'update_pause_status', mock_update_pause_status):
        await public_commands.command_pause_handler(message, command)
    
    mock_update_pause_status.assert_called_once_with(-1001234567890, True)
    
    message.answer.assert_called_once()
    response_text = message.answer.call_args[0][0]
    assert "паузе" in response_text
    assert "/unpause" in response_text


@pytest.mark.asyncio
async def test_command_unpause_handler():
    message = AsyncMock()
    message.chat.id = -1001234567890
    message.from_user.id = 123456789
    message.answer = AsyncMock()
    
    mock_admin = Mock()
    mock_admin.user = Mock()
    mock_admin.user.id = 123456789
    message.bot = AsyncMock(return_value=[mock_admin])
    
    command = AsyncMock()
    command.args = None
    
    mock_telethon_helper = AsyncMock()
    mock_telethon_helper.chat_check = AsyncMock()
    
    mock_update_pause_status = AsyncMock()
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'update_pause_status', mock_update_pause_status), \
         patch.object(public_commands, 'get_chat_status', AsyncMock(return_value=False)):
        
        await public_commands.command_unpause_handler(message, command)
    
    mock_update_pause_status.assert_called_once_with(-1001234567890, False)
    
    mock_telethon_helper.chat_check.assert_called_once_with(-1001234567890)
    
    message.answer.assert_called_once()
    response_text = message.answer.call_args[0][0]
    assert "активирован" in response_text


@pytest.mark.asyncio
async def test_command_add_all_members_handler():
    message = AsyncMock()
    message.chat.id = -1001234567890
    message.from_user.id = 123456789
    message.answer = AsyncMock()
    
    mock_admin = Mock()
    mock_admin.user = Mock()
    mock_admin.user.id = 123456789
    message.bot = AsyncMock(return_value=[mock_admin])
    
    command = AsyncMock()
    command.args = None
    
    mock_telethon_helper = AsyncMock()
    mock_telethon_helper.get_chat_members = AsyncMock(return_value=[
        {'id': 111, 'username': 'user1'},
        {'id': 222, 'username': 'user2'}
    ])
    
    mock_add_user_to_whitelist = AsyncMock(return_value=True)
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'add_user_to_whitelist', mock_add_user_to_whitelist):
        
        await public_commands.command_add_all_members_handler(message, command)
    
    mock_telethon_helper.get_chat_members.assert_called_once_with(-1001234567890)
    
    assert mock_add_user_to_whitelist.call_count == 2
    mock_add_user_to_whitelist.assert_has_calls([
        call(-1001234567890, 111),
        call(-1001234567890, 222)
    ])
    
    message.answer.assert_called_once()
    response_text = message.answer.call_args[0][0]
    assert "добавлены" in response_text


@pytest.mark.asyncio
async def test_command_pause_handler_not_admin():
    message = AsyncMock()
    message.chat.id = -1001234567890
    message.from_user.id = 123456789
    message.answer = AsyncMock()
    
    mock_admin = Mock()
    mock_admin.user = Mock()
    mock_admin.user.id = 999999999
    message.bot = AsyncMock(return_value=[mock_admin])
    
    command = AsyncMock()
    command.args = None
    
    mock_update_pause_status = AsyncMock()
    
    with patch.object(public_commands, 'update_pause_status', mock_update_pause_status):
        await public_commands.command_pause_handler(message, command)
    
    mock_update_pause_status.assert_not_called()
    
    message.answer.assert_called_once()
    response_text = message.answer.call_args[0][0]
    assert "только для админов" in response_text


@pytest.mark.asyncio
async def test_command_unpause_handler_not_admin():
    message = AsyncMock()
    message.chat.id = -1001234567890
    message.from_user.id = 123456789
    message.answer = AsyncMock()
    
    mock_admin = Mock()
    mock_admin.user = Mock()
    mock_admin.user.id = 999999999
    message.bot = AsyncMock(return_value=[mock_admin])
    
    command = AsyncMock()
    command.args = None
    
    mock_update_pause_status = AsyncMock()
    mock_telethon_helper = AsyncMock()
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'update_pause_status', mock_update_pause_status):
        
        await public_commands.command_unpause_handler(message, command)
    
    mock_update_pause_status.assert_not_called()
    mock_telethon_helper.chat_check.assert_not_called()
    
    message.answer.assert_called_once()
    response_text = message.answer.call_args[0][0]
    assert "только для админов" in response_text


@pytest.mark.asyncio
async def test_command_add_all_members_handler_not_admin():
    message = AsyncMock()
    message.chat.id = -1001234567890
    message.from_user.id = 123456789
    message.answer = AsyncMock()
    
    mock_admin = Mock()
    mock_admin.user = Mock()
    mock_admin.user.id = 999999999
    message.bot = AsyncMock(return_value=[mock_admin])
    
    command = AsyncMock()
    command.args = None
    
    mock_telethon_helper = AsyncMock()
    mock_add_user_to_whitelist = AsyncMock()
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'add_user_to_whitelist', mock_add_user_to_whitelist):
        
        await public_commands.command_add_all_members_handler(message, command)
    
    mock_telethon_helper.get_chat_members.assert_not_called()
    mock_add_user_to_whitelist.assert_not_called()
    
    message.answer.assert_called_once()
    response_text = message.answer.call_args[0][0]
    assert "только для админов" in response_text
