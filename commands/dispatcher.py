from aiogram import Dispatcher, Router, F

private_router = Router()
public_router = Router()
basic_router = Router()
dp = Dispatcher()
public_router.message.filter(F.chat.type == "group" or F.chat.type == "supergroup")
private_router.message.filter(F.chat.type == "private")
dp.include_router(public_router)
dp.include_router(private_router)
dp.include_router(basic_router)
