import json
from pathlib import Path
from telegram.update import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler, MessageHandler,
                          ConversationHandler, Filters, CallbackContext, CallbackQueryHandler)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)


json_frasi_path = "./json/frasi.json"
frasi = json.loads(open(json_frasi_path, encoding="utf8").read())


def help(update: Update, context: CallbackContext):
    '''Comando help, spiega cosa fanno i vari comandi e mostra i menu con le varie funzioni:
    - gruppi: reindirizza ai vari gruppi della community
    - social: reindirizza ai canali social della community
    - ho bisogno di assistenza: reindirizza ad un messaggio di aiuto
    - avvisi: -
    - meeting: -
    - \ attivi: mostra i progetti attivi, con rispettivi link, di Mozilla e di Mozilla Italia
    - vademecum: -
    - regolamento: -
    - info: -
    - lascia il tuo feedback: - '''

    buttons = [
        [InlineKeyboardButton(str(frasi["btn_txt_gruppi"]), callback_data="gruppi"),
         InlineKeyboardButton(
             str(frasi["btn_txt_social"]), callback_data="social"),
         InlineKeyboardButton(str(frasi["btn_start2"]), callback_data="supporto")],

        [InlineKeyboardButton(str(frasi["btn_txt_avvisi"]), callback_data="avvisi"),
         InlineKeyboardButton(
             str(frasi["btn_txt_call"]), callback_data="meeting"),
         InlineKeyboardButton(str(frasi["btn_txt_progetti_attivi"]), callback_data="progetti")],

        [InlineKeyboardButton(str(frasi["btn_txt_vademecum"]), callback_data="vademecum"),
         InlineKeyboardButton(
             str(frasi["btn_txt_regolamento"]), callback_data="regolamento"),
         InlineKeyboardButton(str(frasi["btn_txt_info"]), callback_data="info")],

        [InlineKeyboardButton(str(frasi["btn_feedback"]),
                              callback_data="lascia_feedback")]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_markdown(str(frasi["cmd_help"]))
    update.message.reply_text(
        str(frasi["cmd_help2"]), reply_markup=reply_markup, parse_mode="MARKDOWN")
