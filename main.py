from telegram.ext import Defaults, Updater
from telegram import ParseMode
from loguru import logger
from time import sleep
import logging
import pytz

from database.weekly import weekly_run
from config import Config

time_zone = pytz.timezone('America/Sao_Paulo')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@logger.catch
def main():
    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(Config.BOT_TOKEN, defaults=defaults, workers=32)  # type: ignore
    
    j = updater.job_queue
    j.run_once(weekly_run, when=0)

    updater.start_polling(poll_interval=1.0, timeout=5.0)
    sleep(15)
    updater.stop()


if __name__ == '__main__':
    main()
