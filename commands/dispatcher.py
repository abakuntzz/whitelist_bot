from aiogram import Dispatcher, Router, F
from .admin_check import IsAdmin

basic_router = Router()
admin_router = Router()
private_router = Router()
dp = Dispatcher()
admin_router.message.filter(IsAdmin())
private_router.message.filter(F.chat.type == "private")
dp.include_router(basic_router)
dp.include_router(admin_router)
dp.include_router(private_router)
