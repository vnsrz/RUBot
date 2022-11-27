from telegram import Update
from commands.public.download import *
import decorators

def send_pdfs(update: Update, ctx):
    chat_id = update.message.chat_id
    for file in listdir(WD):
        f = path.join(WD, file)
        if path.isfile(f):
            doc = open(f, 'rb')
            ctx.bot.send_document(chat_id, doc)

@decorators.chat_type.private
def executor(update: Update, ctx):
    get_cardapio()
    send_pdfs(update, ctx)
    