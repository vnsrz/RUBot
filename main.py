from telegram.ext import Defaults, Updater
from telegram import ParseMode
from datetime import time
from loguru import logger
import logging
import pytz

from database.weekly import weekly_send, weekly_download
from commands import command_router
from handlers import handler_core
from config import Config

time_zone = pytz.timezone('America/Sao_Paulo')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@logger.catch
def main():
    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(Config.BOT_TOKEN, defaults=defaults, workers=32)  # type: ignore
    dispatcher = updater.dispatcher

    command_router.setup_user_commands(dispatcher)
    command_router.setup_admin_commands(dispatcher)
    handler_core.setup_core_handler(dispatcher)

    j = updater.job_queue

    j.run_repeating(weekly_send, interval=60, first=10)
    #j.run_daily(weekly_download, time=time(hour=12, minute=50 , tzinfo=time_zone), days=('5',))
    #j.run_daily(weekly_send, time=time(hour=13, tzinfo=time_zone), days=('5',))
    
    updater.start_polling(poll_interval=1.0, timeout=5.0)
    updater.idle()


if __name__ == '__main__':
    main()
