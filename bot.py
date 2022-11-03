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
import validators

#логгирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

updater = Updater(SECRET_KEY, use_context=True)
competition = False
code = False


def valid_link(link):
	"""
	Проверяет правильность отправленной ссылки
	:return: true или false
	"""
	return validators.url(link)

def valid_wallet(wallet):
	"""
	Проверяет правильность отправленного id кошелька
	:return: true или false
	"""
	return True if len(wallet) == 42 else False

def valid_nickname(nickname):
	"""
	Проверяет правильность отправленного никнейма пользователя
	:return: true или false
	"""
	return True if "@" in nickname else False

def valid_tokens_data(data):
	"""
	Проверяет правильность отправленного сообщения с ссылкой, кошельком и никнеймом пользователя 
	:return: true или false
	"""
	filtered_data = data.split(" ")
	if valid_link(filtered_data[0]) and valid_nickname(filtered_data[1]) and valid_wallet(filtered_data[2]):
		return True
	else:
		return False

def valid_code_data(data):
	"""
	Тут нужна проверка кода, но до этого момента я не знал по каким критериям проверять этот код
	:return: true или false
	"""
	if 'lol' in data:
		return True
	else:
		return False

def start(update: Update, context: CallbackContext):
	"""
	Функция отправляет welcome text
	"""
	buttons = [[KeyboardButton(BUTTONS["minto_about"])], [KeyboardButton(BUTTONS["free_tokens"])]]
	context.bot.send_message(chat_id=update.effective_chat.id, text=INFO["welcome_text"], reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))

def minto_tokens_answ(update: Update, context: CallbackContext):
	"""
	Функция отправляет сообщение с двумя кнопками, выйграл в соревновании и есть подарочный код
	"""
	buttons = [
        [InlineKeyboardButton(BUTTONS["competition"], callback_data=BUTTONS["competition"]),],
        [InlineKeyboardButton(BUTTONS["code"], callback_data=BUTTONS["code"])],
    ]
	context.bot.send_message(chat_id=update.effective_chat.id, text=INFO["token_text"], reply_markup=InlineKeyboardMarkup(buttons, resize_keyboard=True))

def support_message(update: Update, context: CallbackContext, user_data):
	"""
	Функция отправляет сообщение конкретному пользователю (поле chat id), в данном случае мне :), когда пользователь отправляет данные по выигранному конкурсу
	"""
	buttons = [[InlineKeyboardButton(text="Tokens sended", callback_data="Tokens sended")], [InlineKeyboardButton(text="There's a mistake in user data", callback_data="There's a mistake in user data")]]
	context.bot.send_message(chat_id=398322598, text=user_data, reply_markup=InlineKeyboardMarkup(buttons, resize_keyboard=True))

def message_handler(update: Update, context: CallbackContext):
	"""
	Эта функция отвечает на запросы пользователя
	"""
	global competition, code
	if BUTTONS["minto_about"] in update.message.text:
		update.message.reply_text("It will be in the near future! I promise")
	elif BUTTONS["free_tokens"] in update.message.text:
		minto_tokens_answ(update, context)
	elif competition == True:
		user_message = update.message.text
		if(valid_tokens_data(user_message)):
			competition = False
			buttons = [[InlineKeyboardButton(text="support", callback_data=BUTTONS["support"])]]
			update.message.reply_text(INFO["info_answ"], reply_markup=InlineKeyboardMarkup(buttons, resize_keyboard=True))
			support_message(update, context, user_message)
		else:
			update.message.reply_text(INFO["not_valid_data"])
	elif code:
		user_message = update.message.text
		if(valid_code_data(user_message)):
			code = False
			update.message.reply_text(INFO["info_answ"])
		else:
			update.message.reply_text(INFO["not_valid_data"])
	elif 'thanks' in update.message.text:
		update.message.reply_text("You're welcome")
	else: update.message.reply_text("Your message not clear")

def help(update: Update, context: CallbackContext):
	"""
	Тут должны быть help команды (эта функция должна их присылать по команде /help)
	"""
	update.message.reply_text("The list of commands:")

def token_buttons(update: Update, context: CallbackContext):
    """
    Тут должны быть help команды (эта функция должна их присылать по команде /help)
    """
    query = update.callback_query
    query.answer()
    global competition, code
    if BUTTONS["competition"] in query.data:
        competition=True
        query.edit_message_text(INFO["competition_info"])
    elif BUTTONS["code"] in query.data:
        code = True
        query.edit_message_text(INFO["code_info"])


#Тут перечислены все команды и их обработчики
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('free_tokens', minto_tokens_answ))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
updater.dispatcher.add_handler(CallbackQueryHandler(token_buttons))

updater.start_polling()
