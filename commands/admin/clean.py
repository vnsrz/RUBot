from telegram import Update
from commands.public.download import *
from config import Config
import decorators
import os

def cache_clean(dir):
    for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            try:
                os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

@decorators.chat_type.private
def executor(update: Update, ctx):
    usr = update.message.from_user.id
    if(str(usr) == Config.ADM_ID):
        cache_clean(WD)
        cache_clean(WD2)
        return update.message.reply_text("O cache foi limpo.")
    else:
        return update.message.reply_text("Você não tem permissão para usar esse comando.")