from cgitb import text
import logging
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.filters import Filters
from credentials import SECRET_KEY
from config import BUTTONS, INFO

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

updater = Updater(SECRET_KEY, use_context=True)
competition = False
code = False

def valid_wallet_data(data):
	if 'lol' in data:
		return True
	else:
		return False

def valid_code_data(data):
	if 'lol' in data:
		return True
	else:
		return False

def start(update: Update, context: CallbackContext):
	buttons = [[KeyboardButton(BUTTONS["minto_about"])], [KeyboardButton(BUTTONS["free_tokens"])]]
	context.bot.send_message(chat_id=update.effective_chat.id, text=INFO["welcome_text"], reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))

def minto_tokens_answ(update: Update, context: CallbackContext):
	buttons = [
        [InlineKeyboardButton(BUTTONS["competition"], callback_data="1"),],
        [InlineKeyboardButton(BUTTONS["code"], callback_data="3")],
    ]
	context.bot.send_message(chat_id=update.effective_chat.id, text="!!!", reply_markup=InlineKeyboardMarkup(buttons, resize_keyboard=True))

def message_handler(update: Update, context: CallbackContext):
	global competition, code
	if BUTTONS["minto_about"] in update.message.text:
		update.message.reply_text("It will be in the near future! I promise")
	elif BUTTONS["free_tokens"] in update.message.text:
		context.bot.send_message(chat_id=update.effective_chat.id, text="/free_tokens")
	elif BUTTONS["competition"] in update.message.text:
		competition=True
		update.message.reply_text(INFO["competition_info"])
	elif BUTTONS["code"] in update.message.text:
		code = True
		update.message.reply_text(INFO["code_info"])
	elif competition:
		user_message = update.message.text
		if(valid_wallet_data(user_message)):
			competition = False
			buttons = [[InlineKeyboardButton(text="support")]]
			update.message.reply_text(f"Thanks! Give me up to one hour to check the data. {user_message}", reply_markup=InlineKeyboardMarkup(buttons, resize_keyboard=True))
		else:
			update.message.reply_text("Data isn't valid, send in one more time")
	elif code:
		user_message = update.message.text
		if(valid_code_data(user_message)):
			competition = False
			update.message.reply_text(f"Thanks! Give me up to one hour to check the data. {user_message}")
		else:
			update.message.reply_text("Code isn't valid, send in one more time")
	elif 'thanks' in update.message.text:
		update.message.reply_text("You're welcome")
	else:
		update.message.reply_text("I don't anderstand what are you doing")

def help(update: Update, context: CallbackContext):
	update.message.reply_text("Egor is very cool men (it isn't joke)")

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('free_tokens', minto_tokens_answ))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
