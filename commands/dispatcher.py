from aiogram import Dispatcher, Router, F
from aiogram.enums import ChatType

public_router = Router()
basic_router = Router()
dp = Dispatcher()
public_router.message.filter(F.chat.type.in_
                             ({ChatType.GROUP, ChatType.SUPERGROUP,
                               ChatType.CHANNEL}))
dp.include_router(public_router)
dp.include_router(basic_router)
