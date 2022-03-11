import json
from telegram.update import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler, MessageHandler,
                          ConversationHandler, Filters, CallbackContext, CallbackQueryHandler)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)

json_frasi_path = "./json/frasi.json"
frasi = json.loads(open(json_frasi_path, encoding="utf8").read())


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(frasi["comando_non_riconosciuto"])
