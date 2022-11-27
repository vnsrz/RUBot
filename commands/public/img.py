from telegram import Update
from commands.public.download import *
import decorators

def send_imgs(update: Update, ctx):
    chat_id = update.message.chat_id
    for file in listdir(WD2):
        f = path.join(WD2, file)
        if path.isfile(f):
            pic = open(f, 'rb')
            ctx.bot.send_photo(chat_id, pic)

@decorators.chat_type.private
def executor(update: Update, ctx):
    get_cardapio()
    send_imgs(update, ctx)
    