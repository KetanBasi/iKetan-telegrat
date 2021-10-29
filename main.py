import os
import logging
from ast import literal_eval
from telegram import Update
from telegram.ext import CallbackContext, Updater as BotClient, Updater
from telegram.ext import CommandHandler

from modules.core import c_core
from modules.core.c_core import this_bot
from modules.extensions import x_base

# ? ===============
# ? Logging
# ? ===============
# logging.basicConfig(
# 	filename=f"iKetan Telegrat {c_core.time()}.log",
# 	format="[%(asctime)s | %(levelname)s] %(name)s: %(message)s",
# 	level=logging.DEBUG)
# ? Setup Logging
# ? ===============
logger = logging.getLogger("telegram")
logger.setLevel(logging.DEBUG)

# ? Logging: File Handler
# ? ===============
log_file = os.path.join(
	*[c_core.my_work_dir, f"{this_bot.name} {c_core.time()}.log"])
log_file_handler = logging.FileHandler(
	filename=log_file,
	encoding="utf-8",
	mode="w")
log_file_handler.setLevel(logging.DEBUG)

# ? Logging: Console Handler
# ? ===============
log_console_handler = logging.StreamHandler()
log_console_handler.setLevel(logging.DEBUG)

# ? Logging: Add Handlers
# ? ===============
logger.addHandler(log_file_handler)
logger.addHandler(log_console_handler)

# ! ===============
# ! Logging

# ? ===============
# ? Main Bot
# ? ===============
token_name = "ketan_token"

# bot = telegram.Bot(c_core.get_token(token_name))
bot = BotClient(c_core.get_token(token_name))

dispatcher = bot.dispatcher

# for name, ext in extensions.__dict__.items():
# 	if not name.startswith("_"):
# 		ext.Base(bot)

# for module in os.listdir("modules/extensions"):
# 	if module != "__init__.py" or module[-3:] == ".py":
# 		__import__(f"modules.extensions.{module[:-3]}", locals(), globals())
# 		module[:-3].Base(bot)
# del module

x_base.Base(bot)


# ? Define "/start" command
def start(update: Update, context: CallbackContext):
	context.bot.send_message(
		chat_id=update.effective_chat.id,
		text="I'm a bot, I'm a bot")


# ? Make "/start" command handler
start_handler = CommandHandler("start", start)
# ? Add "/start" command (handler) to the bot
dispatcher.add_handler(start_handler)

# ? Start the bot
bot.start_polling()
