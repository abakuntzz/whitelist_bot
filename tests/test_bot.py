import pytest
from unittest.mock import patch, AsyncMock, Mock, mock_open
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bot.bot_launch as bot_launch
import bot.set_commands as set_commands

@pytest.mark.asyncio
async def test_initialise_commands(mock_bot):
   
    await set_commands.initialise_commands(mock_bot)
    assert mock_bot.set_my_commands.call_count == 2


@pytest.mark.asyncio
async def test_activate():
    mock_telethon_helper = AsyncMock()
    mock_telethon_helper.initialize = AsyncMock()
    mock_telethon_helper.shutdown = AsyncMock()
    
    mock_bot = AsyncMock()
    mock_bot.set_my_commands = AsyncMock()
    
    with patch.object(bot_launch, 'Bot', return_value=mock_bot), \
         patch.object(bot_launch, 'TelethonHelper', return_value=mock_telethon_helper), \
         patch.object(bot_launch, 'create_tables', AsyncMock()), \
         patch.object(bot_launch, 'dp', AsyncMock()), \
         patch.object(bot_launch.dp, 'start_polling', AsyncMock()), \
         patch.object(bot_launch, 'initialise_commands', AsyncMock()), \
         patch('builtins.open', mock_open(read_data="test_bot_token\n12345\ntest_api_hash\n")), \
         patch('bot.bot_launch.Path') as mock_path:
        
        mock_path_instance = Mock()
        mock_path_instance.__truediv__ = Mock(return_value=Mock())
        mock_path.return_value.parent = Mock()
        mock_path.return_value = mock_path_instance
        
        try:
            await bot_launch.activate()
            assert True
        except Exception as e:
            pytest.fail(f"{e}")
