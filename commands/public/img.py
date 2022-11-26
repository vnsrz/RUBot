from telegram import Update
from commands.public.download import *
import decorators

def send_imgs(update: Update, ctx):
    chat_id = update.message.chat_id
    for file in os.listdir(WD2):
        f = os.path.join(WD2, file)
        if os.path.isfile(f):
            pic = open(f, 'rb')
            ctx.bot.send_photo(chat_id, pic)

@decorators.chat_type.private
def executor(update: Update, ctx):
    download_cardapios()
    send_imgs(update, ctx)
    