from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from typing import List, Dict, Optional
import asyncio

class TelethonHelper:
    _instance: Optional['TelethonHelper'] = None
    _client: Optional[TelegramClient] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = None
            cls._instance._initialized = False
        return cls._instance
    
    @property
    def client(self) -> TelegramClient:
        if self._client is None:
            raise RuntimeError("Telethon client not initialized")
        return self._client
    
    async def initialize(self, api_id: int, api_hash: str, bot_token: str):
        """Инициализация Telethon клиента"""
        if self._initialized:
            return 
        self._client = TelegramClient(
            'whitelist_bot_session',
            api_id=api_id,
            api_hash=api_hash
        )
        await self._client.start(bot_token=bot_token)
        self._initialized = True
        print("✅ Telethon клиент запущен")
        me = await self._client.get_me()
    
    async def shutdown(self):
        """Остановка Telethon клиента"""
        if self._client:
            await self._client.disconnect()
            self._client = None
            self._initialized = False
            print("✅ Telethon клиент остановлен")

    async def get_chat_members(self, chat_id: int) -> List[Dict]:
        """Получить всех участников чата"""
        if not self._initialized:
            raise RuntimeError("Telethon клиент не инициализирован")
        members = []
        try:
            print(f"🔄 Получаю участников чата {chat_id}...")
            async for member in self._client.iter_participants(chat_id):
                if member.bot:
                    # continue
                    pass
                is_admin = 0
                if hasattr(member.participant, '__class__'):
                    if isinstance(member.participant, ChannelParticipantAdmin):
                        is_admin = 1
                    elif isinstance(member.participant, ChannelParticipantCreator):
                        is_admin = 2
                members.append({
                    'id': member.id,
                    'username': member.username,
                    'first_name': member.first_name,
                    'last_name': member.last_name or '',
                    'is_admin': is_admin
                })
            print(f"✅ Получено {len(members)} участников")
            return members
            
        except Exception as e:
            print(f"❌ Ошибка получения участников: {e}")
            return []
    
    async def get_chat_members_count(self, chat_id: int) -> int:
        """Получить количество участников чата"""
        try:
            chat = await self._client.get_entity(chat_id)
            if hasattr(chat, 'participants_count'):
                return chat.participants_count
            return 0
        except:
            return 0
    
    async def kick_user(self, chat_id: int, username: str) -> tuple[bool, str]:
        """Кикнуть пользователя по username"""
        try:
            # Убираем @ если есть
            if username.startswith("@"):
                username = username[1:]
            
            # Получаем пользователя
            user = await self._client.get_entity(username)
            
            # Кикаем пользователя
            await self._client.kick_participant(chat_id, user)
            
            return True, f"✅ Пользователь @{username} кикнут"
            
        except Exception as e:
            return False, f"❌ Ошибка: {type(e).__name__}: {str(e)}"
    
    async def add_users_to_whitelist_from_chat(self, chat_id: int) -> tuple[int, int]:
        """Добавить всех пользователей чата в белый список"""
        added = 0
        total = 0
        
        try:
            async for member in self._client.iter_participants(chat_id):
                if member.bot:
                    continue
                
                total += 1
                added += 1  # Для примера
                
                # Здесь ваша логика добавления в БД
                # if await add_to_database(member.id, member.username):
                #     added += 1
            
            return added, total
            
        except Exception as e:
            print(f"Ошибка: {e}")
            return added, total
    
    async def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Получить информацию о пользователе по username"""
        try:
            if username.startswith("@"):
                username = username[1:]
            
            user = await self._client.get_entity(username)
            return {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name or '',
                'is_bot': user.bot if hasattr(user, 'bot') else False
            }
        except Exception as e:
            print(f"Ошибка получения пользователя {username}: {e}")
            return None
    
    async def test_connection(self, chat_id: int = None) -> str:
        """Тест соединения и проверка чата"""
        try:
            me = await self._client.get_me()
            result = f"✅ Telethon работает!\n"
            result += f"Бот: @{me.username} (ID: {me.id})\n"
            
            if chat_id:
                try:
                    chat = await self._client.get_entity(chat_id)
                    result += f"\n📊 Чат {chat_id}:\n"
                    result += f"• Название: {chat.title if hasattr(chat, 'title') else 'Нет'}\n"
                    if hasattr(chat, 'participants_count'):
                        result += f"• Участников: {chat.participants_count}\n"
                    result += f"• Тип: {type(chat).__name__}\n"
                except Exception as e:
                    result += f"\n⚠️ Чат {chat_id} не доступен: {e}\n"
            return result
            
        except Exception as e:
            return f"❌ Ошибка Telethon: {type(e).__name__}: {str(e)}"