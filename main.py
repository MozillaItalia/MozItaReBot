import os
from dotenv import load_dotenv

import logging
from telegram.update import Update
from telegram.update import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler,
                          MessageHandler, ConversationHandler, Filters, CallbackContext)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)

load_dotenv()

TOKEN = os.getenv('TESTTOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = str(
        f"Benvenuto nel bot di Mozilla Italia. Utilizzandomi potrai ottenere informazioni,richiedere supporto e molto altro. Scopri le funzioni a tua disposizione digitando /help.\n \nRicorda di unirti al nostro gruppo utenti Telegram, raggiungici in [Mozilla Italia - Home](https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ)!")
    msg = str(f"Dopo questa breve presentazione, che cosa desideri fare? 😄")
  #  logger.info(f"User: %s", user.first_name, "start the bot")

    buttons = [[InlineKeyboardButton("Mostra che cosa posso fare ➡️", callback_data='1')], [
        InlineKeyboardButton("Ho bisogno di assistenza 🆘", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(buttons)

    update.message.reply_markdown(text)
    update.message.reply_text(msg, reply_markup=reply_markup)


def help(update: Update, context: CallbackContext):
    text = str(
        f"Questa è la lista di comandi a tua disposizione: /start: visualizza il messaggio iniziale.")
    update.message.reply_text(text)


def unknown(update: Update, context: CallbackContext):
    text = str(f"Questo comando non è stato riconosciuto.")
    update.message.reply_text()


def main() -> None:
    updater = Updater(str(TOKEN))

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.text, unknown))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
