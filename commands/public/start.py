from telegram import Update
from database import user_log

def usr_log(usr):
    user_log.Users().write(usr)
    print("New user logged.")

def usr_read(update: Update, ctx):
    usr = str(update.message.from_user.id)
    log = user_log.Users().read()

    if not log.__contains__(usr):
        usr_log(usr)
        
def executor(update: Update, ctx):
    usr_read(update, ctx)
    msg="Bot para facilitar a visualização do cardápio da semana no RU. Atualmente só mostra o cardápio do Gama."
    return update.message.reply_text(msg)