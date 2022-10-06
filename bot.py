from cgitb import text
import logging
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from credentials import SECRET_KEY
from config import BUTTONS, INFO

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

updater = Updater(SECRET_KEY, use_context=True)

def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Hello sir, Welcome to the mitno bot. Please write\
		/help to see the commands available.")
	buttons = [[KeyboardButton(BUTTONS["competition"])], [KeyboardButton(BUTTONS["code"])]]
	context.bot.send_message(chat_id=update.effective_chat.id, text="Hello", reply_markup=ReplyKeyboardMarkup(buttons))

def message_handler(update: Update, context: CallbackContext):
	if BUTTONS["competition"] in update.message.text:
		update.message.reply_text(INFO["competition_info"])
	if BUTTONS["code"] in update.message.text:
		update.message.reply_text(INFO["code_info"])

def help(update: Update, context: CallbackContext):
	update.message.reply_text("Egor is very cool men (it isn't joke)")

def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(f"Sorry I can't recognize you , you said {update.message.text}")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(f"Sorry {update.message.text} is not a valid command")


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

updater.start_polling()
