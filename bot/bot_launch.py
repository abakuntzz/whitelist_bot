import logging
from pathlib import Path
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from commands.telethon_helper import TelethonHelper
from commands.dispatcher import dp
from commands import public_commands, basic_commands, \
    private_commands  # noqa: F401
from .set_commands import initialise_commands
from database.connection import create_tables
import traceback


async def activate() -> None:
    try:
        log = open("log.txt", "a")
        f_str = '[%(asctime)s] %(name)s: [%(levelname)s] %(message)s'
        logging.basicConfig(level=logging.INFO, format=f_str, stream=log)
        directory = Path(__file__).resolve().parent.parent / "secrets"
        with open(directory / "bot_secret.txt") as f:
            bot_token = f.read().strip()
        with open(directory / "api_id.txt") as f:
            api_id = f.read().strip()
        with open(directory / "api_hash.txt") as f:
            api_hash = f.read().strip()
        telethon_helper = TelethonHelper()
        await telethon_helper.initialize(api_id, api_hash, bot_token)
        bot = Bot(token=bot_token,
                  default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp['telethon_helper'] = telethon_helper
        await initialise_commands(bot)
        await create_tables()
        await dp['telethon_helper'].master_check()
        await dp.start_polling(bot)
    except Exception as e:
        print(traceback.format_exc())
        logging.info(f"Ошибка запуска бота - {e}")
    finally:
        try:
            await dp['telethon_helper'].shutdown()
            log.close()
        except Exception as e:
            logging.info(f"Не удалось завершить работу клиента - {e}")
