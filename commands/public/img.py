from os import path, listdir, getcwd
from database.weekly import WD, WD2
from telegram import Update

def send_imgs(update: Update, ctx):
    chat_id = update.message.chat_id
    for file in listdir(WD2):
        f = path.join(WD2, file)
        if path.isfile(f):
            pic = open(f, 'rb')
            ctx.bot.send_photo(chat_id, pic)



def executor(update: Update, ctx):
    send_imgs(update, ctx)
    