from sqlalchemy import select, delete
import logging
from .bd_structure import Chat, Whitelist
from .connection import AsyncSessionLocal


async def add_user_to_whitelist(chat_id: int,
                                user_id: int) -> bool:
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Whitelist).where(
                    (Whitelist.chat_id == chat_id) &
                    (Whitelist.user_id == user_id)
                )
            )
            
            if result.scalar_one_or_none():
                return False  # уже в списке
            entry = Whitelist(chat_id=chat_id, user_id=user_id)
            session.add(entry)
            chat_result = await session.execute(
                select(Chat).where(Chat.id == chat_id)
            )
            if not chat_result.scalar_one_or_none():
                session.add(Chat(id=chat_id, paused=True))
            await session.commit()
            return True
    except Exception as e:
        logging.info(f"Не удалось добавить пользователя {user_id} в список "
                     f"{chat_id} - {e}")
        return False


async def remove_user_from_whitelist(chat_id: int, user_id: int) -> bool:
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                delete(Whitelist).where(
                    (Whitelist.chat_id == chat_id) &
                    (Whitelist.user_id == user_id)
                )
            )
            if result.rowcount > 0:
                await session.commit()
                return True
            else:
                return False
    except Exception as e:
        logging.info(f"Не удалось убрать пользователя {user_id} из списка "
                     f"{chat_id} - {e}")
        return False


async def get_chat_status(chat_id: int) -> bool:
    try:
        async with AsyncSessionLocal() as session:
            chat_result = await session.execute(
                select(Chat).where(Chat.id == chat_id)
            )
            chat = chat_result.scalar_one_or_none()
            if not chat:
                chat = Chat(id=chat_id, paused=True)
                session.add(chat)
                await session.commit()
                return True
            return chat.paused
    except Exception as e:
        logging.info(f"Не удалось получить статус чата {chat_id} - {e}")
        return True


async def update_pause_status(chat_id: int, paused: bool) -> bool:
    try:
        async with AsyncSessionLocal() as session:
            chat_result = await session.execute(
                select(Chat).where(Chat.id == chat_id)
            )
            chat = chat_result.scalar_one_or_none()
            if not chat:
                chat = Chat(id=chat_id, paused=paused)
                session.add(chat)
            else:
                chat.paused = paused
            await session.commit()
            return True
    except Exception as e:
        logging.info(f"Не получилось изменить статус чата {chat_id} на "
                     f"{paused} - {e}")
        return False


async def get_whitelist_by_chat(chat_id: int) -> list[str]:
    async with AsyncSessionLocal() as session:
        whitelist_result = await session.execute(
            select(Whitelist.user_id).where(Whitelist.chat_id == chat_id)
        )
        return [f"{row[0]}" for row in whitelist_result.fetchall()]


async def is_user_in_whitelist(chat_id: int, user_id: int) -> bool:
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Whitelist.id).where(
                    (Whitelist.chat_id == chat_id) &
                    (Whitelist.user_id == user_id)
                )
            )
            return result.scalar_one_or_none() is not None
    except Exception as e:
        logging.info(f"Не удалось проверить наличие пользователя {user_id} "
                     f"в списке {chat_id} - {e}")
        return True
