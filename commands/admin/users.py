from database import user_log
from telegram import Update
from config import Config

import decorators

@decorators.chat_type.private
def executor(update: Update, ctx):
    usr = update.message.from_user.id
    if(str(usr) == Config.ADM_ID):
        qtd = user_log.Users().qtd()
        return update.message.reply_text(f"O bot possui {qtd} usuários.")
    else:
        return update.message.reply_text("Você não tem permissão para usar esse comando.")