import json
import logging
import os
from pathlib import Path

logger = logging.getLogger()


class BaseReader():
    FILE_PATH = ''
    data = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                BaseReader, cls).__new__(cls)
        return cls.instance

    def read_data(self):
        if self.data is None:
            if Path(self.FILE_PATH).exists():
                logger.debug(f'Reading {self.FILE_PATH}...')
                self.data = json.loads(
                    open(self.FILE_PATH, encoding="utf8").read())
            else:
                logger.error(
                    f'File: {os.path.basename(self.FILE_PATH)} non trovato ')
                raise FileNotFoundError
        return self.data


class ListReader(BaseReader):
    FILE_PATH = "./json/liste.json"
    lists = None

    def __init__(self):
        self.lists = self.read_data()

    def get_lists(self):
        return self.lists


class PhrasesReader(BaseReader):
    FILE_PATH = "./json/frasi.json"
    phrases = None

    def __init__(self):
        self.phrases = self.read_data()

    def get_buttons(self):
        return self.phrases['buttons']

    def get_commands(self):
        return self.phrases['commands']

    def get_locations(self):
        return self.phrases['locations']

    def get_actions(self):
        return self.phrases['actions']

    def get_starts(self):
        return self.phrases['starts']
