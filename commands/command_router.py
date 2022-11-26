from telegram.ext import CommandHandler
from commands import public, admin

def setup_user_commands(dispatcher):
    fn = dispatcher.add_handler

    fn(CommandHandler('start', public.start.executor))
    fn(CommandHandler('cardapio', public.cardapio.executor))



def setup_admin_commands(dispatcher):
    pass