import logging
import requests
import os
import json
from telegram.update import Update
from telegram.ext import (CallbackContext, CallbackContext)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from .reader import PhrasesReader, ListReader
from .utils import *

phrases_reader = PhrasesReader()
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
        [InlineKeyboardButton(phrases_buttons["start"], callback_data="help")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    _reply(update, phrases_starts["start"], reply_markup)


def help(update: Update, context: CallbackContext):
    '''Comando help, spiega cosa fanno i vari comandi e mostra i menu con le varie funzioni:
    - gruppi: reindirizza ai vari gruppi della community
    - social: reindirizza ai canali social della community
    - ho bisogno di assistenza: reindirizza ad un messaggio di aiuto
    - progetti: mostra i progetti attivi, con rispettivi link, di Mozilla e di Mozilla Italia
    - vademecum: ottieni il vademecum, il volantino che in poche e semplici parole ti illustra che cosa è Mozilla e i vari progetti attivi.
    - regolamento: per leggere il regolamento comunitario.
    - info: avere informazioni riguardo questo bot.
    - lascia il tuo feedback: permette di lasciare un feedback sul gruppo home '''

    buttons = [
        [InlineKeyboardButton(str(phrases_buttons["testo_gruppi"]), callback_data="gruppi"),
         InlineKeyboardButton(
             str(phrases_buttons["testo_social"]), callback_data="social"),
         InlineKeyboardButton(str(phrases_buttons["start2"]), callback_data="supporto")],

        [InlineKeyboardButton(str(phrases_buttons["testo_progetti_attivi"]), callback_data="progetti"),

         InlineKeyboardButton(str(phrases_buttons["testo_vademecum"]), callback_data="vademecum")],
        [InlineKeyboardButton(
            str(phrases_buttons["regolamento"]), callback_data="regolamento"),
         InlineKeyboardButton(str(phrases_buttons["testo_info"]), callback_data="info")],

        [InlineKeyboardButton(str(phrases_buttons["feedback"]),
                              callback_data="feedback")]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    _reply(update, phrases_commands["help"], None)
    _reply(update, phrases_commands["help2"], reply_markup)


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
    _reply(update, phrases_commands["progetti"], reply_markup)

    buttons.clear()

    for nome_prog_mozita in liste["progetti_mozita"]:
        buttons.append([InlineKeyboardButton(
            nome_prog_mozita, callback_data="progetti", url=liste["progetti_mozita"][str(nome_prog_mozita)])])

    buttons.append([InlineKeyboardButton(
        str(phrases_buttons["back_mostra_help"]),    callback_data="help")])

    reply_markup = InlineKeyboardMarkup(buttons)
    _reply(update, phrases_commands["progetti2"], reply_markup)


def groups(update: Update, context: CallbackContext):
    '''Comando gruppi, mostra i bottoni che rimandano ai gruppi della community.
    Scorre nella lista dei gruppi presa dal file json e crea un bottone con link per ogni gruppo.'''
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


def supporto(update: Update, context: CallbackContext):
    '''Comando attivabile dal bottone "ho bisogno di aiuto" mostra i bottoni che rimandano al gruppo home, al forum e alla pagina delle faq.'''
    buttons = [
        [InlineKeyboardButton(str(phrases_buttons["support"]), url=str(liste["link_gruppi"]["Home 🦊"])),
         InlineKeyboardButton(str(phrases_buttons["support2"]), callback_data="forum")],
        [InlineKeyboardButton(str(phrases_buttons["support3"]), url=str(liste["link_v ari"]["link_faq"]))]]

    buttons.append([InlineKeyboardButton(
        phrases_buttons["back_mostra_help"], callback_data="help")])
    reply_markup = InlineKeyboardMarkup(buttons)
    _reply(update, phrases_commands["supporto"], reply_markup)


def feedback(update: Update, context: CallbackContext):
    '''Comando feedback, mostra un bottone per lasciare un feedback nel gruppo home.'''
    buttons = [
        [InlineKeyboardButton(str(phrases_buttons["feedback"]), callback_data="feedback", url=str(
            liste["link_gruppi"]["Home 🦊"]))],
        [InlineKeyboardButton(str(phrases_buttons["back_mostra_help"]),  callback_data="help")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    _reply(update, phrases_commands["feedback"], reply_markup)


def social(update: Update, context: CallbackContext):
    '''Comando social, mostra bottoni che rimandano direttamente ai social della community.
    Scorre nella lista dei social presa dal file json e crea un bottone con link per ogni social.'''
    buttons = []
    for social_name in liste['social'].keys():
        buttons.append(
            [InlineKeyboardButton(
                text=social_name, callback_data=social_name, url=liste['social'][social_name])]
        )

    buttons.append([InlineKeyboardButton(
        phrases_buttons["back_mostra_help"], callback_data="help")])
    reply_markup = InlineKeyboardMarkup(buttons)

    _reply(update, phrases_commands["social"], reply_markup)


def vademecum(update: Update, context: CallbackContext):
    '''Comando vademeucm, mostra i bottoni per scaricare il Vademecum Generale, Tecnico e di Common Voice'''
    buttons = [
        [InlineKeyboardButton(str(phrases_buttons["vg"]), callback_data="vademecum_generale"),
         InlineKeyboardButton(str(phrases_buttons["vt"]), callback_data="vademecum_tecnico")],
        [InlineKeyboardButton(str(phrases_buttons["vcv"]),
                              callback_data="vademecum_cv")],
        [InlineKeyboardButton(str(phrases_buttons["back_mostra_help"]),  callback_data="help")]]

    reply_markup = InlineKeyboardMarkup(buttons)
    _reply(update, phrases_commands["vademecum"], reply_markup)


def vademecum_cv(update, context):
    '''Invia il Vademecum di Common Voice sotto forma di file pdf scaricandolo dal repo di Mozilla Italia.'''
    chat_id = get_chat_id(update, context)
    buttons = [[InlineKeyboardButton(
        str(phrases_buttons["back_mostra_help"]),  callback_data="help")]]
    try:
        download_file(liste["link_vademecum"]["Vademecum Common Voice"])
    except requests.exceptions.RequestException:
        _reply(update, phrases_actions["qualcosa_e_andato_storto"], None)
        exit()
    _reply(update,  phrases_actions["vademecum_invio_in_corso"], None)
    reply_markup = InlineKeyboardMarkup(buttons)

    context.bot.send_document(chat_id, document=open("resources/"+str(os.path.basename(
        liste["link_vademecum"]["Vademecum Common Voice"])), "rb"), timeout=100)
    _reply(update, phrases_actions["consulta_vcv"], reply_markup)


def vademecum_generale(update, context):
    '''Invia il Vademecum Generale sotto forma di file pdf scaricandolo dal repo di Mozilla Italia.'''
    chat_id = get_chat_id(update, context)
    buttons = [[InlineKeyboardButton(
        str(phrases_buttons["back_mostra_help"]),  callback_data="help")]]

    _reply(update,  phrases_actions["vademecum_invio_in_corso"], None)
    reply_markup = InlineKeyboardMarkup(buttons)
    try:
        download_file(liste["link_vademecum"]["Vademecum Generale"])
    except requests.exceptions.RequestException:
        _reply(update, phrases_actions["qualcosa_e_andato_storto"], None)
        exit()

    context.bot.send_document(chat_id, document=open(
        "resources/"+str(os.path.basename(liste["link_vademecum"]["Vademecum Generale"])), "rb"), timeout=100)
    _reply(update, phrases_actions["consulta_vg"], reply_markup)


def vademecum_tecnico(update, context):
    '''Invia il Vademecum Tecnico sotto forma di file pdf scaricandolo dal repo di Mozilla Italia.'''
    chat_id = get_chat_id(update, context)
    buttons = [[InlineKeyboardButton(
        str(phrases_buttons["back_mostra_help"]),  callback_data="help")]]

    _reply(update,  phrases_actions["vademecum_invio_in_corso"], None)
    reply_markup = InlineKeyboardMarkup(buttons)
    try:
        download_file(liste["link_vademecum"]["Vademecum Tecnico"])
    except requests.exceptions.RequestException:
        _reply(update, phrases_actions["qualcosa_e_andato_storto"], None)
        exit()

    context.bot.send_document(chat_id, document=open(
        "resources/"+str(os.path.basename(liste["link_vademecum"]["Vademecum Tecnico"])), "rb"), timeout=100)
    _reply(update, phrases_actions["consulta_vt"], reply_markup)


def forum(update: Update, context: CallbackContext):
    '''Comando forum, mostra il bottone che rimanda al forum della community.'''
    buttons = [
        [InlineKeyboardButton(str(phrases_buttons["forum"]),
                              url=liste['social']["Forum"])]]
    buttons.append([InlineKeyboardButton(
        phrases_buttons["back_mostra_help"], callback_data="help")])
    reply_markup = InlineKeyboardMarkup(buttons)
    _reply(update, phrases_locations["forum"], reply_markup)


def regolamento(update: Update, context: CallbackContext):
    '''Comando regolamento, mostra un messaggio con il regolamento scaricandolo dal repo di Mozilla Italia.'''
    try:
        download_file(liste['link_vari']["link_regolamento"])
    except requests.exceptions.RequestException:
        _reply(update, phrases_actions["qualcosa_e_andato_storto"], None)
        exit()
    buttons = [[InlineKeyboardButton(
        str(phrases_buttons["back_mostra_help"]), callback_data="help")]]
    f = open("resources/" +
             str(os.path.basename(liste['link_vari']["link_regolamento"])), "r")

    reply_markup = InlineKeyboardMarkup(buttons)
    _reply(update, f.read(), reply_markup)


def info(update: Update, context: CallbackContext):
    ''' Comando info, mostra le informazioni di sviluppo del bot, versione, ultimo aggiornamento e collabboratori che vengono presi direttamente tramite le API di github'''
    chat_id = get_chat_id(update, context)
    buttons = []
    try:
        download_file(liste['link_vari']["link_contributors"])
    except requests.exceptions.RequestException:
        _reply(update, phrases_actions["qualcosa_e_andato_storto"], None)
        exit()

    f = open("resources/" +
             str(os.path.basename(liste['link_vari']["link_contributors"])), "r")
    data = json.load(f)

    new_string = phrases_commands["info"].format(
        versione="2.0", ultimo_aggiornamento="ieri")    # placeholders temporanei

    format_string = "[{username}]({account_url})"
    temp_string = ""
    for i in data:
        temp_string += " " + \
            format_string.format(
                username=i["login"], account_url=i["html_url"])
    new_string = new_string+temp_string

    buttons.append([InlineKeyboardButton(
        str(phrases_buttons["back_mostra_help"]),    callback_data="help")])

    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id, text=new_string, disable_web_page_preview=True,
                             parse_mode='MARKDOWN', reply_markup=reply_markup)
