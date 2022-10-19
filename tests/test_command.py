
from src.reader import PhrasesReader, ListReader


def test_start(bot, user):
    user.send_command('/start')
    message = user.get_message()
    start_phrases = PhrasesReader().get_starts()
    assert message
    assert message['text'] == start_phrases['start']


def test_unknown(bot, user):
    user.send_command('/testmessagenotfound')
    message = user.get_message()
    command_phrases = PhrasesReader().get_commands()
    assert message
    assert message['text'] == command_phrases['comando_non_riconosciuto']


def test_groups(bot, user):
    user.send_command('/gruppi')
    message = user.get_message()
    command_phrases = PhrasesReader().get_commands()
    assert message
    assert message['text'] == command_phrases['gruppi']


def test_regolamento(bot, user):
    user.send_command('/regolamento')
    message = user.get_message()
    command_phrases = PhrasesReader().get_commands()
    assert message
    assert message['text'] == command_phrases['regolamento']


def test_progetti(bot, user):
    user.send_command('/progetti')
    message = user.get_message()
    command_phrases = PhrasesReader().get_commands()
    assert message
    assert message['text'] == command_phrases['progetti']
