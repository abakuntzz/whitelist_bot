import pytest
import sys
import os
from aiogram.types import BotCommandScopeAllGroupChats, BotCommandScopeDefault

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bot.set_commands as set_commands   # noqa: E402


@pytest.mark.asyncio
async def test_initialise_commands(mock_bot) -> None:
    await set_commands.initialise_commands(mock_bot)
    assert mock_bot.set_my_commands.call_count == 2

    calls = mock_bot.set_my_commands.call_args_list
    first_commands = calls[0][1]['commands']
    first_scope = calls[0][1]['scope']
    second_commands = calls[1][1]['commands']
    second_scope = calls[1][1]['scope']

    assert isinstance(first_scope, BotCommandScopeAllGroupChats)
    assert len(first_commands) == 7
    assert isinstance(second_scope, BotCommandScopeDefault)
    assert len(second_commands) == 2
