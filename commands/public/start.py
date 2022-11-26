from telegram import Update
import decorators

@decorators.chat_type.private
def executor(update: Update, ctx):
    msg="Bot para facilitar a visualização do cardápio da semana no RU. Atualmente só mostra o cardápio do Gama."
    return update.message.reply_text(msg)