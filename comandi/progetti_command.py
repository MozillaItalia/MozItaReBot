
import json
from pathlib import Path
from telegram.update import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler, MessageHandler,
                          ConversationHandler, Filters, CallbackContext, CallbackQueryHandler)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)


json_frasi_path = "./json/frasi.json"
json_liste_path = "./json/liste.json"

if Path(json_frasi_path).exists():
    frasi = json.loads(open(json_frasi_path, encoding="utf8").read())
else:
    print("File frasi non presente.")
    exit()

if Path(json_liste_path).exists():
    liste = json.loads(open(json_liste_path, encoding="utf8").read())
else:
    print("File liste non presente.")
    exit()


def progetti(update: Update, context: CallbackContext):
    '''Comando progetti, mostra i progetti attivi, con rispettivi link, di Mozilla e di Mozilla Italia.
    Scorre nella lista dei progetti presa dal file json e crea un bottone con link per ogni progetto.'''

    buttons = []
    for nome_prog_moz in liste["progetti"]:

        buttons.append([InlineKeyboardButton(
            nome_prog_moz, callback_data="progetti", url=liste["progetti"][str(nome_prog_moz)])])

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(
        str(frasi["cmd_progetti"]), reply_markup=reply_markup)

    buttons.clear()  # questa cosa si ptrebbe fare con udue variabili diverese (es. buttons e buttons2) ma in questo omdo utilizzo la stessa avriabile per tutti i bottoni del bot per favorire eventuali manutenzioni e sviluppi futuri
    for nome_porg_mozita in liste["progetti_mozita"]:

        buttons.append([InlineKeyboardButton(nome_porg_mozita, callback_data="progetti",
                       url=liste["progetti_mozita"][str(nome_porg_mozita)])])

    buttons.append([InlineKeyboardButton(
        str(frasi["button_back_mostra_help"]),    callback_data="help")])

    update.message.reply_text(
        str(frasi["cmd_progetti2"]), reply_markup=reply_markup)
