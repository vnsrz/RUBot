from telegram import Update

import decorators

@decorators.chat_type.private
def executor(update: Update, ctx):
    return update.message.reply_text("Hello, world!")