import asyncio
import logging
import sys
from bot.bot_launch import activate

if __name__ == "__main__":
    log = open("log.txt", "a")
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(name)s: [%(levelname)s] %(message)s', stream=log)
    asyncio.run(activate())
