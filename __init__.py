import asyncio
import logging
import sys
from bot.bot_launch import activate

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(activate())
