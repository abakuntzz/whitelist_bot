from aiogram.filters import Filter
from aiogram.types import Message
from aiogram import Bot

class IsAdmin(Filter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        if message.chat.type not in ["group", "supergroup"]:
            return False
        try:
            chat_member = await bot.get_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id
            )
            return chat_member.status in ["creator", "administrator"]
        except Exception as e:
            print(f"Error checking admin status: {e}")
            return False
