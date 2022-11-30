import logging
import schedule
from loguru import logger
from telegram import ParseMode
from telegram.ext import Defaults, Updater, CallbackContext
from time import sleep

from commands import command_router
from config import Config
from handlers import handler_core

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def callback_minute(context: CallbackContext):
    context.bot.send_message(chat_id='81509534', 
                             text='One message every minute')

@logger.catch
def main():
    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(Config.BOT_TOKEN, defaults=defaults, workers=32)  # type: ignore
    dispatcher = updater.dispatcher

    command_router.setup_user_commands(dispatcher)
    command_router.setup_admin_commands(dispatcher)
    handler_core.setup_core_handler(dispatcher)

    j = updater.job_queue
    job_minute = j.run_repeating(callback_minute, interval=30, first=10)

    updater.start_polling(poll_interval=1.0, timeout=5.0)
    updater.idle()

if __name__ == '__main__':
    main()
