
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


def handler_groups(update: Update, context: CallbackContext):
    # '''
    #     Handler per tutti i comandi dei gruppi. Restituisce un messaggio di testo e un bottone con un link al gruppo scelto.
    #     Es. /home -> messaggio di presentazione del gruppo home e bottone che rimanda al gruppo home
    # '''

    # # bisogna capire di che comando si tratta
    # # dell'intero messaggio, prendi solo la parte dopo lo / e prima di uno spazio
    # # (i comandi sono gestiti dall'handler e saranno sempre nella forma '/cmd param1')
    # # (note: there probably is a better way to achieve this)

    # cmd = update.message.text.encode('utf-8').decode().split(" ")[0][1:]

    # buttons = []
    # txt = ""

    # match cmd:
    #     case "home":
    #         buttons = [
    #             [InlineKeyboardButton(str(frasi["btn_home"]), url=str(
    #                 liste["link_gruppi"]["home"]), callback_data="home")]
    #         ]
    #         txt = str(frasi["cmd_home"])

    #     case "news":
    #         buttons = [
    #             [InlineKeyboardButton(str(frasi["btn_news"]), url=str(
    #                 liste["link_gruppi"]["news"]), callback_data="news")]
    #         ]
    #         txt = str(frasi["cmd_news"])

    #     case "dev" | "developers" | "sviluppo":
    #         buttons = [
    #             [InlineKeyboardButton(str(frasi["btn_developers"]), url=str(
    #                 liste["link_gruppi"]["developers"]), callback_data="dev")]
    #         ]
    #         txt = str(frasi["cmd_dev"])

    #     case "dem" | "design" | "marketing":
    #         buttons = [
    #             [InlineKeyboardButton(str(frasi["btn_dem"]), url=str(
    #                 liste["link_gruppi"]["dem"]), callback_data="dem")]
    #         ]
    #         txt = str(frasi["cmd_dem"])

    #     case "lion" | "l10n":
    #         buttons = [
    #             [InlineKeyboardButton(str(frasi["btn_l10n"]), url=str(
    #                 liste["link_gruppi"]["l10n"]), callback_data="l10n")]
    #         ]
    #         txt = str(frasi["cmd_l10n"])

    #     case _:
    #         buttons = []
    #         txt = "Caro sviluppatore, hai dimenticato di gestire questo handler. Crea un nuovo case e definisci bottone e testo.\n\n_\"Ottimo! Ma hai lasciato degli oggetti alle tue spalle...\"_\n- Merlin Munroe"

    # reply_markup = InlineKeyboardMarkup(buttons)
    # update.message.reply_text(
    #     txt, reply_markup=reply_markup, parse_mode="MARKDOWN")


    #
    print("")