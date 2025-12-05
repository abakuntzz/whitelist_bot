from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .bd_stucture import Chat, Whitelist
from .connection import AsyncSessionLocal


async def add_user_to_whitelist(username: str, chat_id: int) -> tuple[bool, str]:
    async with AsyncSessionLocal() as session:
        username_clean = username.lower().replace('@', '')
        result = await session.execute(
            select(Whitelist).where(
                (Whitelist.chat_id == chat_id) & 
                (Whitelist.username == username_clean)
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            return False, f"@{username_clean} уже в белом списке"
          
        entry = Whitelist(chat_id=chat_id, username=username_clean)
        session.add(entry)

        chat_result = await session.execute(
            select(Chat).where(Chat.id == chat_id)
        )
        if not chat_result.scalar_one_or_none():
            session.add(Chat(id=chat_id, paused=True))
        
        await session.commit()
        return True, f"@{username_clean} добавлен"
        
async def add_user_to_whitelist(username: str, chat_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        username_clean = username.lower().replace('@', '')
        result = await session.execute(
            select(Whitelist).where(
                (Whitelist.chat_id == chat_id) & 
                (Whitelist.username == username_clean)
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            return False  # Уже в списке
  
        entry = Whitelist(chat_id=chat_id, username=username_clean)
        session.add(entry)
        # Убедимся что чат существует
        chat_result = await session.execute(
            select(Chat).where(Chat.id == chat_id)
        )
        if not chat_result.scalar_one_or_none():
            session.add(Chat(id=chat_id, paused=True))
        
        await session.commit()
        return True

async def remove_user_from_whitelist(username: str, chat_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        username_clean = username.lower().replace('@', '') 
        result = await session.execute(
            delete(Whitelist).where(
                (Whitelist.chat_id == chat_id) & 
                (Whitelist.username == username_clean)
            )
        )
        
        if result.rowcount > 0:
            await session.commit()
            return True  
        else:
            return False


async def get_chat_status(chat_id: int) -> bool:
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


async def update_pause_status(chat_id: int, paused: bool) -> bool:
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

async def get_whitelist_by_chat(chat_id: int) -> list[str]:
    async with AsyncSessionLocal() as session:
        whitelist_result = await session.execute(
            select(Whitelist.username).where(Whitelist.chat_id == chat_id)
        )
        return [f"@{row[0]}" for row in whitelist_result.fetchall()]
      
async def is_user_in_whitelist(username: str, chat_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        username_clean = username.lower().replace('@', '')
    
        result = await session.execute(
            select(Whitelist.id).where(
                (Whitelist.chat_id == chat_id) & 
                (Whitelist.username == username_clean)
            )
        )
        return result.scalar_one_or_none() is not None
