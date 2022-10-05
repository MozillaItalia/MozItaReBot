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

load_dotenv()
TOKEN = os.getenv("TESTTOKEN")


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

phrases_notices = frasi['notices']
phrases_buttons = frasi['buttons']
phrases_commands = frasi['commands']
phrases_locations = frasi['locations']
phrases_actions = frasi['actions']
phrases_starts = frasi['starts']

def start(update: Update, context: CallbackContext):
    '''Comando start, mostra messaggio di benvenuto e indirizza al menu'''
    buttons = [
        [InlineKeyboardButton(str(phrases_buttons["button_start"]), callback_data="help")]]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(
        str(phrases_starts["start"]), reply_markup=reply_markup, parse_mode="MARKDOWN")


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
        [InlineKeyboardButton(str(phrases_buttons["testo_gruppi"]), callback_data="gruppi"),
         InlineKeyboardButton(
             str(phrases_buttons["testo_social"]), callback_data="social"),
         InlineKeyboardButton(str(phrases_buttons["start2"]), callback_data="supporto")],

        [InlineKeyboardButton(str(phrases_buttons["testo_avvisi"]), callback_data="avvisi"),
         InlineKeyboardButton(
             str(phrases_buttons["testo_call"]), callback_data="meeting"),
         InlineKeyboardButton(str(phrases_buttons["testo_progetti_attivi"]), callback_data="progetti")],

        [InlineKeyboardButton(str(phrases_buttons["testo_progetti_attivi"]), callback_data="vademecum"),
         InlineKeyboardButton(
             str(phrases_buttons["regolamento"]), callback_data="regolamento"),
         InlineKeyboardButton(str(phrases_buttons["testo_info"]), callback_data="info")],

        [InlineKeyboardButton(str(phrases_buttons["feedback"]),
                              callback_data="lascia_feedback")]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_markdown(str(phrases_commands["help"]))
    update.message.reply_text(
        str(phrases_commands["help2"]), reply_markup=reply_markup, parse_mode="MARKDOWN")


def unknown(update: Update, context: CallbackContext):
    '''In caso il comando passato non venga riconosciuto, restituisce un opportuno messaggio di errore'''
    update.message.reply_text(phrases_commands["comando_non_riconosciuto"])


def progetti(update: Update, context: CallbackContext):
    '''Comando progetti, mostra i progetti attivi, con rispettivi link, di Mozilla e di Mozilla Italia.
    Scorre nella lista dei progetti presa dal file json e crea un bottone con link per ogni progetto.'''

    query = update.callback_query
    buttons = []

    for nome_prog_moz in liste["progetti"]:

        buttons.append([InlineKeyboardButton(
            nome_prog_moz, callback_data="progetti", url=liste["progetti"][str(nome_prog_moz)])])

    reply_markup = InlineKeyboardMarkup(buttons)

    if not hasattr(update.callback_query, "inline_message_id"):
        update.message.reply_text(
            str(phrases_commands["progetti"]), reply_markup=reply_markup, parse_mode="MARKDOWN")
    else:
        query.answer()
        query.message.reply_text(
            str(phrases_commands["progetti"]), reply_markup=reply_markup, parse_mode="MARKDOWN")

    buttons.clear()

    for nome_prog_mozita in liste["progetti_mozita"]:
        buttons.append([InlineKeyboardButton(
            nome_prog_mozita, callback_data="progetti", url=liste["progetti_mozita"][str(nome_prog_mozita)])])

    buttons.append([InlineKeyboardButton(
        str(phrases_buttons["back_mostra_help"]),    callback_data="help")])

    reply_markup = InlineKeyboardMarkup(buttons)

    if not hasattr(update.callback_query, "inline_message_id"):
        update.message.reply_text(
            str(phrases_commands["progetti2"]), reply_markup=reply_markup, parse_mode="MARKDOWN")
    else:
        query.answer()
        query.message.reply_text(
            str(phrases_commands["progetti2"]), reply_markup=reply_markup, parse_mode="MARKDOWN")


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
            [InlineKeyboardButton(str(phrases_buttons["home"]), url=str(
                liste["link_gruppi"]["home"]), callback_data="home")]
        ]
        txt = str(phrases_commands["home"])

    elif cmd == "news":
        buttons = [
            [InlineKeyboardButton(str(phrases_buttons["news"]), url=str(
                liste["link_gruppi"]["news"]), callback_data="news")]
        ]
        txt = str(phrases_commands["news"])

    elif cmd == "dev" or cmd == "developers" or cmd == "sviluppo":
        buttons = [
            [InlineKeyboardButton(str(phrases_buttons["developers"]), url=str(
                liste["link_gruppi"]["developers"]), callback_data="dev")]
        ]
        txt = str(phrases_commands["dev"])

    elif cmd == "dem" or cmd == "design" or cmd == "marketing":
        buttons = [
            [InlineKeyboardButton(str(phrases_buttons["dem"]), url=str(
                liste["link_gruppi"]["dem"]), callback_data="dem")]
        ]
        txt = str(phrases_commands["dem"])

    elif cmd == "lion" or cmd == "l10n":
        buttons = [
            [InlineKeyboardButton(str(phrases_buttons["l10n"]), url=str(
                liste["link_gruppi"]["l10n"]), callback_data="l10n")]
        ]
        txt = str(phrases_commands["l10n"])

    else:
        buttons = []
        txt = "Caro sviluppatore, hai dimenticato di gestire questo handler. Crea un nuovo case e definisci bottone e testo.\n\n_\"Ottimo! Ma hai lasciato degli oggetti alle tue spalle...\"_\n- Merlin Munroe"

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(
        txt, reply_markup=reply_markup, parse_mode="MARKDOWN")


def buttons_handler(update: Update, context: CallbackContext):
    '''Cattura il click di un bottone per generare un nuovo messaggio'''

    query = update.callback_query
    query.answer()

    if str(query.data).lower() == "help":
        query.message.reply_markdown(str(phrases_commands["help"]))
        buttons = [
            [InlineKeyboardButton(str(phrases_buttons["testo_gruppi"]), callback_data="gruppi"),
             InlineKeyboardButton(
                 str(phrases_buttons["testo_social"]), callback_data="social"),
             InlineKeyboardButton(str(phrases_buttons["start2"]), callback_data="supporto")],

            [InlineKeyboardButton(str(phrases_buttons["testo_avvisi"]), callback_data="avvisi"),
             InlineKeyboardButton(
                 str(phrases_buttons["testo_call"]), callback_data="meeting"),
             InlineKeyboardButton(str(phrases_buttons["testo_progetti_attivi"]), callback_data="progetti")],

            [InlineKeyboardButton(str(phrases_buttons["testo_vademecum"]), callback_data="vademecum"),
             InlineKeyboardButton(
                 str(phrases_buttons["testo_regolamento"]), callback_data="regolamento"),
             InlineKeyboardButton(str(phrases_buttons["testo_info"]), callback_data="info")],

            [InlineKeyboardButton(
                str(phrases_buttons["feedback"]), callback_data="lascia_feedback")]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)
        query.message.reply_text(
            str(phrases_commands["help2"]), reply_markup=reply_markup)

    elif str(query.data).lower() == "supporto":
        buttons = [
            [InlineKeyboardButton(str(phrases_buttons["support"]), url=str(liste["link_gruppi"]["home"])),
             InlineKeyboardButton(str(phrases_buttons["support2"]), callback_data="forum")],
            [InlineKeyboardButton(str(phrases_buttons["support3"]),
                                  url="https://forum.mozillaitalia.org/index.php?board=9.0")],
            [InlineKeyboardButton(
                str(phrases_buttons["back_mostra_help"]), callback_data="help")]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)
        query.message.reply_markdown(
            str(phrases_commands["supporto"]),  reply_markup=reply_markup)

    elif str(query.data).lower() == "forum":
        buttons = [
            [InlineKeyboardButton(str(phrases_buttons["forum"]),
                                  url="https://forum.mozillaitalia.org/")],
            [InlineKeyboardButton(str(phrases_buttons["back_mostra_help"]), callback_data="help")]]

        reply_markup = InlineKeyboardMarkup(buttons)
        query.message.reply_markdown(
            str(phrases_locations["forum"]),  reply_markup=reply_markup)

    elif str(query.data).lower() == "progetti":
        buttons = []
        progetti(update, context)


def main() -> None:

    updater = Updater(str(TOKEN))
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("progetti", progetti))

    # comandi che rimandano a gruppi (comandi redirect)
    # alias:
    #       può capitare che un utente si sbagli o chiami un gruppo con un nome diverso (o più corto)
    #       per questo sono stati aggiunti dei nomi più comodi.
    #       Ex. /sviluppo e /dev hanno lo stesso comportamento.
    # nota:
    #       ogni alias va aggiunto nell'handler, altrimenti non succederà nulla
    dp.add_handler(CommandHandler("home", handler_groups))
    dp.add_handler(CommandHandler("news", handler_groups))

    dp.add_handler(CommandHandler("dev", handler_groups))
    dp.add_handler(CommandHandler("developers", handler_groups))
    dp.add_handler(CommandHandler("sviluppo", handler_groups))

    dp.add_handler(CommandHandler("dem", handler_groups))
    dp.add_handler(CommandHandler("design", handler_groups))
    dp.add_handler(CommandHandler("marketing", handler_groups))
    dp.add_handler(CommandHandler("designmarketing", handler_groups))

    dp.add_handler(CommandHandler("lion", handler_groups))
    dp.add_handler(CommandHandler("l10n", handler_groups))

    dp.add_handler(MessageHandler(Filters.text, unknown))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_handler(CallbackQueryHandler(buttons_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
