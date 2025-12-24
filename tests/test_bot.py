import pytest
from unittest.mock import patch, AsyncMock, Mock, mock_open
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bot.set_commands as set_commands   # noqa: E402


@pytest.mark.asyncio
async def test_initialise_commands(mock_bot) -> None:
    await set_commands.initialise_commands(mock_bot)
    assert mock_bot.set_my_commands.call_count == 2
