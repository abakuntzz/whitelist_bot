import pytest
from unittest.mock import patch, call, AsyncMock, Mock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import commands.public_commands as public_commands


@pytest.mark.asyncio
async def test_command_list_handler_empty(mock_message):
    mock_get_whitelist_by_chat = AsyncMock(return_value=[])
    mock_get_chat_status = AsyncMock(return_value=False)
    
    with patch.object(public_commands, 'get_whitelist_by_chat', mock_get_whitelist_by_chat), \
         patch.object(public_commands, 'get_chat_status', mock_get_chat_status), \
         patch.object(public_commands, 'dp', {'telethon_helper': AsyncMock()}):
        
        await public_commands.command_list_handler(mock_message)
    
    mock_message.answer.assert_called_once()
    response_text = mock_message.answer.call_args[0][0]
    assert "Белый список:" in response_text
    assert "Пусто..." in response_text
    assert "<b>Статус:</b> ON." in response_text


@pytest.mark.asyncio
async def test_command_list_handler_with_users(mock_message, mock_telethon_helper):
    mock_get_whitelist_by_chat = AsyncMock(return_value=['111', '222'])
    mock_get_chat_status = AsyncMock(return_value=True)
    
    mock_telethon_helper.get_user_by_id.side_effect = [
        {'first_name': 'John', 'last_name': 'Doe', 'username': 'john'},
        {'first_name': 'Jane', 'last_name': 'Smith', 'username': 'jane'}
    ]
    
    with patch.object(public_commands, 'get_whitelist_by_chat', mock_get_whitelist_by_chat), \
         patch.object(public_commands, 'get_chat_status', mock_get_chat_status), \
         patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}):
        
        await public_commands.command_list_handler(mock_message)
    
    mock_message.answer.assert_called_once()
    response_text = mock_message.answer.call_args[0][0]
    assert "Белый список:" in response_text
    assert "John Doe (john)" in response_text
    assert "Jane Smith (jane)" in response_text
    assert "<b>Статус:</b> OFF." in response_text


@pytest.mark.asyncio
async def test_command_add_user_handler(mock_message_admin, mock_command):
    mock_command.args = "@username"
    
    mock_telethon_helper = AsyncMock()
    mock_telethon_helper.get_user_by_username = AsyncMock(return_value={'id': 555, 'username': 'testuser'})
    
    mock_add_user_to_whitelist = AsyncMock(return_value=True)
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'add_user_to_whitelist', mock_add_user_to_whitelist):
        
        await public_commands.command_add_user_handler(mock_message_admin, mock_command)
    
    mock_telethon_helper.get_user_by_username.assert_called_once_with("@username")
    mock_add_user_to_whitelist.assert_called_once_with(-1001234567890, 555)
    mock_message_admin.answer.assert_called_once()
    assert "добавлен в белый список" in mock_message_admin.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_command_add_user_handler_no_args(mock_message_admin, mock_command):
    mock_command.args = None
    
    await public_commands.command_add_user_handler(mock_message_admin, mock_command)
    
    mock_message_admin.answer.assert_called_once()
    response_text = mock_message_admin.answer.call_args[0][0]
    assert "не передали параметр" in response_text
    assert "/add_user @user" in response_text


@pytest.mark.asyncio
async def test_command_add_user_handler_user_already_exists(mock_message_admin, mock_command):
    mock_command.args = "@username"
    
    mock_telethon_helper = AsyncMock()
    mock_telethon_helper.get_user_by_username = AsyncMock(return_value={'id': 555, 'username': 'testuser'})
    
    mock_add_user_to_whitelist = AsyncMock(return_value=False)
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'add_user_to_whitelist', mock_add_user_to_whitelist):
        
        await public_commands.command_add_user_handler(mock_message_admin, mock_command)
    
    mock_message_admin.answer.assert_called_once()
    assert "уже в белом списке" in mock_message_admin.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_command_remove_user_handler(mock_message_admin, mock_command):
    mock_command.args = "@username"
    
    mock_telethon_helper = AsyncMock()
    mock_telethon_helper.get_user_by_username = AsyncMock(return_value={'id': 555, 'username': 'testuser'})
    mock_telethon_helper.kick_user = AsyncMock(return_value=True)
    
    mock_remove_user_from_whitelist = AsyncMock(return_value=True)
    mock_get_chat_status = AsyncMock(return_value=False)
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'remove_user_from_whitelist', mock_remove_user_from_whitelist), \
         patch.object(public_commands, 'get_chat_status', mock_get_chat_status):
        
        await public_commands.command_remove_user_handler(mock_message_admin, mock_command)
    
    mock_telethon_helper.get_user_by_username.assert_called_once_with("@username")
    mock_remove_user_from_whitelist.assert_called_once_with(-1001234567890, 555)
    mock_telethon_helper.kick_user.assert_called_once_with(-1001234567890, 555)
    mock_message_admin.answer.assert_called_once()
    assert "удалён из белого списка" in mock_message_admin.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_command_remove_user_handler_user_not_found(mock_message_admin, mock_command):
    mock_command.args = "@username"
    
    mock_telethon_helper = AsyncMock()
    mock_telethon_helper.get_user_by_username = AsyncMock(return_value={'id': 555, 'username': 'testuser'})
    
    mock_remove_user_from_whitelist = AsyncMock(return_value=False)
    mock_get_chat_status = AsyncMock(return_value=False)
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'remove_user_from_whitelist', mock_remove_user_from_whitelist), \
         patch.object(public_commands, 'get_chat_status', mock_get_chat_status):
        
        await public_commands.command_remove_user_handler(mock_message_admin, mock_command)
    
    mock_message_admin.answer.assert_called_once()
    assert "не найден в белом списке" in mock_message_admin.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_command_unpause_handler(mock_message_admin, mock_command, mock_telethon_helper):
    mock_update_pause_status = AsyncMock()
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'update_pause_status', mock_update_pause_status):
        
        await public_commands.command_unpause_handler(mock_message_admin, mock_command)
    
    mock_update_pause_status.assert_called_once_with(-1001234567890, False)
    mock_telethon_helper.chat_check.assert_called_once_with(-1001234567890)
    mock_message_admin.answer.assert_called_once()
    assert "активирован" in mock_message_admin.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_command_add_all_members_handler(mock_message_admin, mock_command, mock_telethon_helper):
    mock_telethon_helper.get_chat_members.return_value = [
        {'id': 111, 'username': 'user1'},
        {'id': 222, 'username': 'user2'}
    ]
    
    mock_add_user_to_whitelist = AsyncMock(return_value=True)
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'add_user_to_whitelist', mock_add_user_to_whitelist):
        
        await public_commands.command_add_all_members_handler(mock_message_admin, mock_command)
    
    mock_telethon_helper.get_chat_members.assert_called_once_with(-1001234567890)
    assert mock_add_user_to_whitelist.call_count == 2
    mock_add_user_to_whitelist.assert_has_calls([
        call(-1001234567890, 111),
        call(-1001234567890, 222)
    ])
    mock_message_admin.answer.assert_called_once()
    assert "добавлены" in mock_message_admin.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_command_unpause_handler_not_admin(mock_message_user, mock_command, mock_telethon_helper):
    mock_update_pause_status = AsyncMock()
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'update_pause_status', mock_update_pause_status):
        
        await public_commands.command_unpause_handler(mock_message_user, mock_command)
    
    mock_update_pause_status.assert_not_called()
    mock_telethon_helper.chat_check.assert_not_called()
    mock_message_user.answer.assert_called_once()
    assert "только для админов" in mock_message_user.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_command_add_all_members_handler_not_admin(mock_message_user, mock_command, mock_telethon_helper):
    mock_add_user_to_whitelist = AsyncMock()
    
    with patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}), \
         patch.object(public_commands, 'add_user_to_whitelist', mock_add_user_to_whitelist):
        
        await public_commands.command_add_all_members_handler(mock_message_user, mock_command)
    
    mock_telethon_helper.get_chat_members.assert_not_called()
    mock_add_user_to_whitelist.assert_not_called()
    mock_message_user.answer.assert_called_once()
    assert "только для админов" in mock_message_user.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_command_remove_all_members_handler(mock_message_admin, mock_command, mock_telethon_helper):
    mock_get_whitelist_by_chat = AsyncMock(return_value=['111', '222', '333'])
    mock_remove_user_from_whitelist = AsyncMock(return_value=True)
    mock_get_chat_status = AsyncMock(return_value=False)
    
    with patch.object(public_commands, 'get_whitelist_by_chat', mock_get_whitelist_by_chat), \
         patch.object(public_commands, 'remove_user_from_whitelist', mock_remove_user_from_whitelist), \
         patch.object(public_commands, 'get_chat_status', mock_get_chat_status), \
         patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}):
        
        await public_commands.command_remove_all_members_handler(mock_message_admin, mock_command)
    
    assert mock_remove_user_from_whitelist.call_count == 3
    mock_remove_user_from_whitelist.assert_has_calls([
        call(-1001234567890, 111),
        call(-1001234567890, 222),
        call(-1001234567890, 333)
    ])
    mock_telethon_helper.chat_check.assert_called_once_with(-1001234567890)
    mock_message_admin.answer.assert_called_once()
    assert "успешно очищен" in mock_message_admin.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_handle_new_chat_member_not_paused_not_in_whitelist(mock_telethon_helper):
    event = AsyncMock()
    event.chat.id = -1001234567890
    event.new_chat_member.user.id = 123456789
    event.answer = AsyncMock()
    
    mock_get_chat_status = AsyncMock(return_value=False)
    mock_is_user_in_whitelist = AsyncMock(return_value=False)
    
    mock_telethon_helper.kick_user = AsyncMock(return_value=True)
    
    with patch.object(public_commands, 'get_chat_status', mock_get_chat_status), \
         patch.object(public_commands, 'is_user_in_whitelist', mock_is_user_in_whitelist), \
         patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}):
        
        await public_commands.handle_new_chat_member(event)
    
    mock_get_chat_status.assert_called_once_with(-1001234567890)
    mock_is_user_in_whitelist.assert_called_once_with(-1001234567890, 123456789)
    mock_telethon_helper.kick_user.assert_called_once_with(-1001234567890, 123456789)
    event.answer.assert_called_once()
    assert "нет в белом списке" in event.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_handle_new_chat_member_paused(mock_telethon_helper):
    event = AsyncMock()
    event.chat.id = -1001234567890
    event.new_chat_member.user.id = 123456789
    event.answer = AsyncMock()
    
    mock_get_chat_status = AsyncMock(return_value=True)
    mock_is_user_in_whitelist = AsyncMock()
    
    with patch.object(public_commands, 'get_chat_status', mock_get_chat_status), \
         patch.object(public_commands, 'is_user_in_whitelist', mock_is_user_in_whitelist), \
         patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}):
        
        await public_commands.handle_new_chat_member(event)
    
    mock_get_chat_status.assert_called_once_with(-1001234567890)
    mock_is_user_in_whitelist.assert_not_called()
    mock_telethon_helper.kick_user.assert_not_called()
    event.answer.assert_not_called()


@pytest.mark.asyncio
async def test_handle_new_chat_member_in_whitelist(mock_telethon_helper):
    event = AsyncMock()
    event.chat.id = -1001234567890
    event.new_chat_member.user.id = 123456789
    event.answer = AsyncMock()
    
    mock_get_chat_status = AsyncMock(return_value=False)
    mock_is_user_in_whitelist = AsyncMock(return_value=True)
    
    with patch.object(public_commands, 'get_chat_status', mock_get_chat_status), \
         patch.object(public_commands, 'is_user_in_whitelist', mock_is_user_in_whitelist), \
         patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}):
        
        await public_commands.handle_new_chat_member(event)
    
    mock_get_chat_status.assert_called_once_with(-1001234567890)
    mock_is_user_in_whitelist.assert_called_once_with(-1001234567890, 123456789)
    mock_telethon_helper.kick_user.assert_not_called()
    event.answer.assert_not_called()


@pytest.mark.asyncio
async def test_bot_added_to_chat():
    event = AsyncMock()
    event.chat.id = -1001234567890
    
    mock_update_pause_status = AsyncMock()
    
    with patch.object(public_commands, 'update_pause_status', mock_update_pause_status):
        await public_commands.bot_added_to_chat(event)
    
    mock_update_pause_status.assert_called_once_with(-1001234567890, True)


@pytest.mark.asyncio
async def test_handle_unadmin_not_paused_not_in_whitelist(mock_telethon_helper):
    event = AsyncMock()
    event.chat.id = -1001234567890
    event.new_chat_member.user.id = 123456789
    
    mock_get_chat_status = AsyncMock(return_value=False)
    mock_is_user_in_whitelist = AsyncMock(return_value=False)
    
    with patch.object(public_commands, 'get_chat_status', mock_get_chat_status), \
         patch.object(public_commands, 'is_user_in_whitelist', mock_is_user_in_whitelist), \
         patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}):
        
        await public_commands.handle_unadmin(event)
    
    mock_get_chat_status.assert_called_once_with(-1001234567890)
    mock_is_user_in_whitelist.assert_called_once_with(-1001234567890, 123456789)
    mock_telethon_helper.kick_user.assert_called_once_with(-1001234567890, 123456789)


@pytest.mark.asyncio
async def test_handle_unadmin_paused(mock_telethon_helper):
    event = AsyncMock()
    event.chat.id = -1001234567890
    event.new_chat_member.user.id = 123456789
    
    mock_get_chat_status = AsyncMock(return_value=True)
    mock_is_user_in_whitelist = AsyncMock()
    
    with patch.object(public_commands, 'get_chat_status', mock_get_chat_status), \
         patch.object(public_commands, 'is_user_in_whitelist', mock_is_user_in_whitelist), \
         patch.object(public_commands, 'dp', {'telethon_helper': mock_telethon_helper}):
        
        await public_commands.handle_unadmin(event)
    
    mock_get_chat_status.assert_called_once_with(-1001234567890)
    mock_is_user_in_whitelist.assert_not_called()
    mock_telethon_helper.kick_user.assert_not_called()
