from telegram import Update

def executor(update: Update, ctx):
    msg="""/start : mensagem inicial
/img : retorna uma imagem com o cardápio do almoço
/pdf : retorna o cardápio completo em formato pdf
/help : lista os comandos"""
    return update.message.reply_text(msg)