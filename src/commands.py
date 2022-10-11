import logging
from telegram.update import Update
from telegram.ext import (CallbackContext, CallbackContext)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from .reader import PhrasesReader, ListReader

phrases_reader = PhrasesReader()
phrases_notices = phrases_reader.get_notices()
phrases_buttons = phrases_reader.get_buttons()
phrases_commands = phrases_reader.get_commands()
phrases_locations = phrases_reader.get_locations()
phrases_actions = phrases_reader.get_actions()
phrases_starts = phrases_reader.get_starts()

lists_reader = ListReader()
liste = lists_reader.get_lists()


def _reply(update: Update, text: str, reply_markup: InlineKeyboardMarkup, parse_mode='MARKDOWN'):
    if not hasattr(update.callback_query, "inline_message_id"):
        update.message.reply_text(
            text, reply_markup=reply_markup, parse_mode=parse_mode)
    else:
        query = update.callback_query
        query.answer()
        query.message.reply_text(
            text, reply_markup=reply_markup, parse_mode=parse_mode)


def start(update: Update, context: CallbackContext):
    '''Comando start, mostra messaggio di benvenuto e indirizza al menu'''
    buttons = [
        [InlineKeyboardButton(str(phrases_buttons["start"]), callback_data="help")]]

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
    _reply(update, phrases_commands["comando_non_riconosciuto"], None)


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


def groups(update: Update, context: CallbackContext):
    buttons = []
    for group_name in liste['link_gruppi'].keys():
        buttons.append(
            [InlineKeyboardButton(
                text=group_name, callback_data=group_name, url=liste['link_gruppi'][group_name])]
        )

    buttons.append([InlineKeyboardButton(
        phrases_buttons["back_mostra_help"], callback_data="help")])
    reply_markup = InlineKeyboardMarkup(buttons)

    _reply(update, phrases_commands["gruppi"], reply_markup)
