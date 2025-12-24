import pytest
from unittest.mock import patch, Mock
import database.commands as db_commands


@pytest.mark.asyncio
async def test_add_user_to_whitelist(mock_db_session) -> None:
    mock_result1 = Mock()
    mock_result1.scalar_one_or_none.return_value = None

    mock_result2 = Mock()
    mock_result2.scalar_one_or_none.return_value = None

    mock_db_session.execute.side_effect = [mock_result1, mock_result2]

    with patch.object(db_commands, 'AsyncSessionLocal') as mock_session_local:
        mock_session_local.return_value.__aenter__.return_value = (
            mock_db_session
        )

        result = await db_commands.add_user_to_whitelist(
            chat_id=-1001234567890,
            user_id=123456789
        )

        assert result is True
        assert mock_db_session.execute.await_count == 2


@pytest.mark.asyncio
async def test_remove_user_from_whitelist(mock_db_session) -> None:
    mock_result = Mock()
    mock_result.rowcount = 1
    mock_db_session.execute.return_value = mock_result

    with patch.object(db_commands, 'AsyncSessionLocal') as mock_session_local:
        mock_session_local.return_value.__aenter__.return_value = (
            mock_db_session
        )

        result = await db_commands.remove_user_from_whitelist(
            chat_id=-1001234567890,
            user_id=123456789
        )

        assert result is True
        mock_db_session.execute.assert_awaited_once()
        mock_db_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_chat_status(mock_db_session) -> None:
    mock_result = Mock()
    mock_chat = Mock()
    mock_chat.paused = True
    mock_result.scalar_one_or_none.return_value = mock_chat

    mock_db_session.execute.return_value = mock_result

    with patch.object(db_commands, 'AsyncSessionLocal') as mock_session_local:
        mock_session_local.return_value.__aenter__.return_value = (
            mock_db_session
        )

        result = await db_commands.get_chat_status(chat_id=-1001234567890)

        assert result is True
        mock_db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_pause_status(mock_db_session) -> None:
    mock_result = Mock()
    mock_chat = Mock()
    mock_chat.paused = False
    mock_result.scalar_one_or_none.return_value = mock_chat

    mock_db_session.execute.return_value = mock_result

    with patch.object(db_commands, 'AsyncSessionLocal') as mock_session_local:
        mock_session_local.return_value.__aenter__.return_value = (
            mock_db_session
        )

        result = await db_commands.update_pause_status(
            chat_id=-1001234567890,
            paused=True
        )

        assert result is True
        mock_db_session.execute.assert_awaited_once()
        assert mock_chat.paused is True
        mock_db_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_whitelist_by_chat(mock_db_session) -> None:
    mock_result = Mock()
    mock_result.fetchall.return_value = [(123456,), (789012,)]
    mock_db_session.execute.return_value = mock_result

    with patch.object(db_commands, 'AsyncSessionLocal') as mock_session_local:
        mock_session_local.return_value.__aenter__.return_value = (
            mock_db_session
        )

        result = await db_commands.get_whitelist_by_chat(
            chat_id=-1001234567890
        )

        assert result == ["123456", "789012"]
        mock_db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_is_user_in_whitelist(mock_db_session) -> None:
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = Mock()
    mock_db_session.execute.return_value = mock_result

    with patch.object(db_commands, 'AsyncSessionLocal') as mock_session_local:
        mock_session_local.return_value.__aenter__.return_value = (
            mock_db_session
        )

        result = await db_commands.is_user_in_whitelist(
            chat_id=-1001234567890,
            user_id=123456789
        )

        assert result is True
        mock_db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_connection() -> None:
    try:
        from database.connection import engine
        async with engine.connect() as conn:
            assert conn is not None
    except Exception as e:
        pytest.fail(f"Не удалось подключиться к БД: {e}")
