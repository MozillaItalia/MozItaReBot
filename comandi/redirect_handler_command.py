
import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv
import logging
from telegram.update import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler, MessageHandler,
                          ConversationHandler, Filters, CallbackContext, CallbackQueryHandler)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)

json_frasi_path = "./json/frasi.json"
json_liste_path = "./json/liste.json"

frasi = json.loads(open(json_frasi_path, encoding="utf8").read())
liste = json.loads(open(json_liste_path, encoding="utf8").read())


def handler_groups(update: Update, context: CallbackContext):
    '''
        Handler per tutti i comandi dei gruppi. Restituisce un messaggio di testo e un bottone con un link al gruppo scelto.
        Es. /home -> messaggio di presentazione del gruppo home e bottone che rimanda al gruppo home
    '''

    # bisogna capire di che comando si tratta
    # dell'intero messaggio, prendi solo la parte dopo lo / e prima di uno spazio
    # (i comandi sono gestiti dall'handler e saranno sempre nella forma '/cmd param1')
    # (note: there probably is a better way to achieve this)
    cmd = update.message.text.encode('utf-8').decode().split(" ")[0][1:]

    buttons = []
    txt = ""

    if cmd == "home":
        buttons = [
            [InlineKeyboardButton(str(frasi["btn_home"]), url=str(
                liste["link_gruppi"]["home"]), callback_data="home")]
        ]
        txt = str(frasi["cmd_home"])
    elif cmd == "news":
        buttons = [
            [InlineKeyboardButton(str(frasi["btn_news"]), url=str(
                liste["link_gruppi"]["news"]), callback_data="news")]
        ]
        txt = str(frasi["cmd_news"])
    elif cmd == "dev" or cmd == "developers" or cmd == "sviluppo":
        buttons = [
            [InlineKeyboardButton(str(frasi["btn_developers"]), url=str(
                liste["link_gruppi"]["developers"]), callback_data="dev")]
        ]
        txt = str(frasi["cmd_dev"])
    elif cmd == "lion" or cmd == "l10n":
        buttons = [
            [InlineKeyboardButton(str(frasi["btn_l10n"]), url=str(
                liste["link_gruppi"]["l10n"]), callback_data="l10n")]
        ]
        txt = str(frasi["cmd_l10n"])
    else:
        buttons = []
        txt = "Caro sviluppatore, hai dimenticato di gestire questo handler. Crea un nuovo case e definisci bottone e testo.\n\n_\"Ottimo! Ma hai lasciato degli oggetti alle tue spalle...\"_\n- Merlin Munroe"

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(
        txt, reply_markup=reply_markup, parse_mode="MARKDOWN")
