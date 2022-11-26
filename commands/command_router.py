from telegram.ext import CommandHandler
from commands import public, admin

def setup_user_commands(dispatcher):
    fn = dispatcher.add_handler

    fn(CommandHandler('start', public.start.executor))
    fn(CommandHandler('help', public.help.executor))
    fn(CommandHandler('pdf', public.pdf.executor))
    fn(CommandHandler('img', public.img.executor))


def setup_admin_commands(dispatcher):
    fn = dispatcher.add_handler

    fn(CommandHandler('clean', admin.clean.executor))
