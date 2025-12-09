from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantAdmin, \
    ChannelParticipantCreator
from typing import List, Dict, Optional
import logging
from database.commands import is_user_in_whitelist


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
        self._me = await self._client.get_me()

    async def shutdown(self):
        """Остановка Telethon клиента"""
        if self._client:
            await self._client.disconnect()
            self._client = None
            self._initialized = False

    async def get_chat_members(self, chat_id: int) -> List[Dict]:
        """Получить всех участников чата"""
        members = []
        try:
            async for member in self._client.iter_participants(chat_id):
                if member.bot:
                    # continue
                    pass
                is_admin = 0
                if hasattr(member.participant, '__class__'):
                    if isinstance(member.participant, ChannelParticipantAdmin):
                        is_admin = 1
                    elif isinstance(member.participant,
                                    ChannelParticipantCreator):
                        is_admin = 2
                members.append({
                    'id': member.id,
                    'username': member.username,
                    'first_name': member.first_name,
                    'last_name': member.last_name or '',
                    'is_admin': is_admin
                })
            return members
        except Exception as e:
            logging.info(f"Ошибка получения участников чата {chat_id} - {e}")
            return []

    async def kick_user(self, chat_id: int, user_id: int) -> bool:
        """Кикнуть пользователя по user_id"""
        try:
            if user_id != self._me.id:
                user = await self._client.get_entity(user_id)
                await self._client.kick_participant(chat_id, user)
                return True
            return False
        except Exception as e:
            logging.info(f"Ошибка кика пользователя {user_id} из чата "
                         f"{chat_id} - {e}")
            return False

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
            logging.info(f"Ошибка получения пользователя {username} - {e}")
            return None

    async def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Получить информацию о пользователе по user_id"""
        try:
            user = await self._client.get_entity(user_id)
            return {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name or '',
                'is_bot': user.bot if hasattr(user, 'bot') else False
            }
        except Exception as e:
            logging.info(f"Ошибка получения пользователя {user_id} - {e}")
            return None

    async def chat_check(self, chat_id: int) -> bool:
        """Проверить соответствие чата chat_id списку"""
        users = await self.get_chat_members(chat_id)
        try:
            for user in users:
                okay = await is_user_in_whitelist(chat_id, user['id'])
                if not okay:
                    try:
                        await self.kick_user(chat_id, user['id'])
                    except Exception as e:
                        logging.info(f"Ошибка кика пользователя {user['id']} "
                                     f"из чата {chat_id} - {e}")
            return True
        except Exception as e:
            logging.info(f"Ошибка проверки чата {chat_id} - {e}")
            return False

    async def master_check(self) -> None:
        """Проверить все чаты на соответствие списку"""
        chats = []  # потом убрать
        # chats = await find_unique_chat_ids()
        for chat_id in chats:
            try:
                me = await self._client.get_me()
                my_status = await self._client.get_permissions(chat_id, me)
                if my_status:
                    await self.chat_check(chat_id)
            except Exception:
                pass
        logging.info("Проверка всех списков окончена")
