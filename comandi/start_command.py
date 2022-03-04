from telegram.update import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler, MessageHandler,
                          ConversationHandler, Filters, CallbackContext, CallbackQueryHandler)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from pathlib import Path
import json


json_frasi_path = "./json/frasi.json"

if Path(json_frasi_path).exists():
    frasi = json.loads(open(json_frasi_path, encoding="utf8").read())
else:
    print("File frasi non presente.")
    exit()


def start(update: Update, context: CallbackContext):
    '''Comando start, mostra messaggio di benevnuto e indirizza al menu'''

    buttons = [
        [InlineKeyboardButton(str(frasi["button_start"]), callback_data="help")]]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(str(frasi["start"]), reply_markup=reply_markup)
