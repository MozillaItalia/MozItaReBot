import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv
import logging
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


file_path = './json/frasi.json'
# loading sentences from file

if Path(file_path).is_file():
    frasi = json.loads(open(file_path, encoding="utf8").read())
else:
    print("File frasi non presente.")
    exit()


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = str(frasi["start"])

    buttons = [[InlineKeyboardButton(str(frasi["button_start"]), callback_data='1')], [InlineKeyboardButton(str(frasi["button_start2"]), callback_data='2')]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_markdown(text)
    update.message.reply_text(str(frasi["start2"]), reply_markup=reply_markup)




def help(update: Update, context: CallbackContext):
    update.message.reply_markdown(str(frasi["cmd_help"]))


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(frasi["comando_non_riconosciuto"])


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
