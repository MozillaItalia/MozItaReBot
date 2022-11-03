import os
from typing import Optional

from dotenv import load_dotenv
import logging
from telegram.update import Update
from telegram.ext import (Updater, CallbackContext, CommandHandler, MessageHandler,
                          Filters, CallbackQueryHandler)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)

from src.reader import ListReader, PhrasesReader
from src.commands import rules, start, help, unknown, progetti, groups, supporto, feedback, social, forum
load_dotenv()
TOKEN = os.getenv("TOKEN")

# logging.basicConfig(level=logging.DEBUG)

try:
    phrases_reader = PhrasesReader()
    phrases_notices = phrases_reader.get_notices()
    phrases_buttons = phrases_reader.get_buttons()
    phrases_commands = phrases_reader.get_commands()
    phrases_locations = phrases_reader.get_locations()
    phrases_actions = phrases_reader.get_actions()
    phrases_starts = phrases_reader.get_starts()
except FileNotFoundError:
    exit()

try:
    lists_reader = ListReader()
    liste = lists_reader.get_lists()
except FileNotFoundError:
    exit()


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

    logging.debug(f'Cliked buttons: {query.data}')
    clicked_button = str(query.data).lower()

    if clicked_button == "help":
        help(update, context)

    elif clicked_button == "supporto":
        supporto(update, context)

    elif clicked_button == "forum":
        forum(update, context)

    elif clicked_button == "progetti":
        progetti(update, context)

    elif clicked_button == 'gruppi':
        groups(update, context)

    elif clicked_button == 'regolamento':
        rules(update, context)

    elif clicked_button == 'feedback':
        feedback(update, context)

    elif clicked_button == 'social':
        social(update, context)

    else:
        unknown(update, context)


def start_bot(token: str, base_url: str = None) -> None:

    updater = Updater(token, base_url)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("progetti", progetti))
    dispatcher.add_handler(CommandHandler("gruppi", groups))
    dispatcher.add_handler(CommandHandler("supporto", supporto))
    dispatcher.add_handler(CommandHandler("regolamento", rules))
    dispatcher.add_handler(CommandHandler("feedback", feedback))
    dispatcher.add_handler(CommandHandler("social", social))
    dispatcher.add_handler(CommandHandler("forum", forum))

    # comandi che rimandano a gruppi (comandi redirect)
    # alias:
    #       può capitare che un utente si sbagli o chiami un gruppo con un nome diverso (o più corto)
    #       per questo sono stati aggiunti dei nomi più comodi.
    #       Ex. /sviluppo e /dev hanno lo stesso comportamento.
    # nota:
    #       ogni alias va aggiunto nell'handler, altrimenti non succederà nulla

    dispatcher.add_handler(CommandHandler("home", handler_groups))
    dispatcher.add_handler(CommandHandler("news", handler_groups))

    dispatcher.add_handler(CommandHandler("dev", handler_groups))
    dispatcher.add_handler(CommandHandler("developers", handler_groups))
    dispatcher.add_handler(CommandHandler("sviluppo", handler_groups))

    dispatcher.add_handler(CommandHandler("dem", handler_groups))
    dispatcher.add_handler(CommandHandler("design", handler_groups))
    dispatcher.add_handler(CommandHandler("marketing", handler_groups))
    dispatcher.add_handler(CommandHandler("designmarketing", handler_groups))

    dispatcher.add_handler(CommandHandler("lion", handler_groups))
    dispatcher.add_handler(CommandHandler("l10n", handler_groups))

    dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(CallbackQueryHandler(buttons_handler))

    updater.start_polling()

    return updater


def main() -> None:
    updater = start_bot(TOKEN, )
    updater.idle()


if __name__ == "__main__":
    main()
