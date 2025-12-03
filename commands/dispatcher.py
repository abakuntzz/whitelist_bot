from aiogram import Dispatcher, Router, F
from aiogram.enums import ChatType

private_router = Router()
public_router = Router()
basic_router = Router()
dp = Dispatcher()
#public_router.message.filter(F.chat.type == "group" or F.chat.type == "supergroup")
public_router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP})) # aiogram 3.22.0
private_router.message.filter(F.chat.type == "private")
dp.include_router(public_router)
dp.include_router(private_router)
dp.include_router(basic_router)
