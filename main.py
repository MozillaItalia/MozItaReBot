import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv
import logging
from telegram.update import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackContext, CallbackQueryHandler)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)

load_dotenv()
TOKEN = os.getenv("TESTTOKEN")

json_frasi_path = "./json/frasi.json"
if Path(json_frasi_path).exists():
    frasi = json.loads(open(json_frasi_path, encoding="utf8").read())
else:
    print("File frasi non presente.")
    exit()


def start(update: Update, context: CallbackContext):

    buttons = [
        [InlineKeyboardButton(str(frasi["button_start"]), callback_data="help"),
         InlineKeyboardButton(str(frasi["button_start2"]), callback_data="supporto")]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_markdown(str(frasi["start"]))
    update.message.reply_text(str(frasi["start2"]), reply_markup=reply_markup)


def help(update: Update, context: CallbackContext):
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


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(frasi["comando_non_riconosciuto"])


def buttons_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if str(query.data).lower() == "help":
        query.message.reply_markdown(str(frasi["cmd_help"]))
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

            [InlineKeyboardButton(
                str(frasi["button_feedback"]), callback_data="lascia_feedback")]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)
        query.message.reply_text(
            str(frasi["cmd_help2"]), reply_markup=reply_markup)
    elif str(query.data).lower() == "supporto":
        buttons = [
            [InlineKeyboardButton(str(frasi["button_support"]), url="https://t.me/joinchat/BCql3UMy26nl4qxuRecDsQ"),
             InlineKeyboardButton(str(frasi["button_support2"]), callback_data="forum")],
            [InlineKeyboardButton(str(frasi["button_support3"]),
                                  url="https://forum.mozillaitalia.org/index.php?board=9.0")],
            [InlineKeyboardButton(
                str(frasi["button_back_mostra_help"]), callback_data="help")]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)
        query.message.reply_markdown(
            str(frasi["cmd_supporto"]),  reply_markup=reply_markup)

    elif str(query.data).lower() == "forum":
        buttons = [
            [InlineKeyboardButton(str(frasi["button_forum"]),
                                  url="https://forum.mozillaitalia.org/")],
            [InlineKeyboardButton(str(frasi["button_back_mostra_help"]), callback_data="help")]]

        reply_markup = InlineKeyboardMarkup(buttons)
        query.message.reply_markdown(
            str(frasi["forum"]),  reply_markup=reply_markup)


def main() -> None:

    updater = Updater(str(TOKEN))

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, unknown))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_handler(CallbackQueryHandler(buttons_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
