from telegram.update import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler, MessageHandler,
                          ConversationHandler, Filters, CallbackContext, CallbackQueryHandler)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from pathlib import Path
import json


json_frasi_path = "./json/frasi.json"
frasi = json.loads(open(json_frasi_path, encoding="utf8").read())


def start(update: Update, context: CallbackContext):
    '''Comando start, mostra messaggio di benvenuto e indirizza al menu'''
    buttons = [
        [InlineKeyboardButton(str(frasi["btn_start"]), callback_data="help")]]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(
        str(frasi["start"]), reply_markup=reply_markup, parse_mode="MARKDOWN")
