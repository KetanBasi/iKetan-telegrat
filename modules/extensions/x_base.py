from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext


def add(bot: Updater, trigger: str, func):
    # bot.dispatcher.add_handler(trigger, func)
    bot.dispatcher.add_handler(CommandHandler(trigger, func))


def Base(bot: Updater):
    def sup(update: Update, context: CallbackContext):
        update.message.reply_text(f"Hello {update.effective_user.first_name}")
    
    def hi(update: Update, context: CallbackContext):
        update.message.reply_text("Sup")
    
    def get_ctx(update: Update, context: CallbackContext):
        update.message.reply_text(str(context))
    
    def get_update(update: Update, context: CallbackContext):
        update.message.reply_text(str(update))
    
    def get_message(update: Update, context: CallbackContext):
        update.message.reply_text(str(update.message))
    
    add(bot, "get_message", get_message)
    add(bot, "get_update", get_update)
    add(bot, "get_ctx", get_ctx)
    add(bot, "hi", hi)
    add(bot, "sup", sup)
