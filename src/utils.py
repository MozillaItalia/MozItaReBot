import logging
import requests
import os
from telegram.update import Update


def get_chat_id(update, context):
    chat_id = -1
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    return chat_id


def download_file(url):
    req = requests.get(url)
    file = open("resurces/"+str(os.path.basename(url)),
                "wb").write(req.content)
    return file
