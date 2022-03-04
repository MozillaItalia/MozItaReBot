import json
from pathlib import Path
from telegram.update import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler, MessageHandler,
                          ConversationHandler, Filters, CallbackContext, CallbackQueryHandler)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)


json_frasi_path = "./json/frasi.json"

if Path(json_frasi_path).exists():
    frasi = json.loads(open(json_frasi_path, encoding="utf8").read())
else:
    print("File frasi non presente.")
    exit()


def help(update: Update, context: CallbackContext):
    '''Comando help, spiega ocsa fanno i vari comandi e mostra i menu con le varie funzioni:
    - gruppi: reinirizza ai vari gruppi della community
    - social: reinirizza ai canali social della community
    - ho bisogno di assistenza: reinirizza ad un messaggio di aiuto
    - avvisi: -
    - meeting: -
    - progetti attivi: mostra i progetti attivi, con rispettivi link, di Mozilla e di Mozilla Italia
    - vademecum: -
    - regolamento: -
    - info: -  
    - lascia il tuo feedback: - '''

    buttons = [
        [InlineKeyboardButton(str(frasi["button_testo_gruppi"]), callback_data="gruppi"),
         InlineKeyboardButton(
             str(frasi["button_testo_social"]), callback_data="social"),
         InlineKeyboardButton(str(frasi["button_start2"]), callback_data="supporto")],

        [InlineKeyboardButton(str(frasi["button_testo_avvisi"]), callback_data="avvisi"),
         InlineKeyboardButton(
             str(frasi["button_testo_call"]), callback_data="meeting"),
         InlineKeyboardButton(str(frasi["button_testo_progetti_attivi"]), callback_data="progetti")],

        [InlineKeyboardButton(str(frasi["button_testo_vademecum"]), callback_data="vademecum"),
         InlineKeyboardButton(
             str(frasi["button_testo_regolamento"]), callback_data="regolamento"),
         InlineKeyboardButton(str(frasi["button_testo_info"]), callback_data="info")],

        [InlineKeyboardButton(str(frasi["button_feedback"]),
                              callback_data="lascia_feedback")]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_markdown(str(frasi["cmd_help"]))
    update.message.reply_text(
        str(frasi["cmd_help2"]), reply_markup=reply_markup)
