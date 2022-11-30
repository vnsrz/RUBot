from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    ADM_ID = os.environ.get('ADM_ID')
    CHAT_ID = os.environ.get('CHAT_ID')