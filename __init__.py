import asyncio

try:
    from bot.bot_launch import activate
except Exception:
    pass
if __name__ == "__main__":
    asyncio.run(activate())
