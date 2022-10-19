from telegram_bot_unittest.core import core
from telegram_bot_unittest.user import Tester, UserBase, ChatBase
from telegram_bot_unittest.user import BOT_TOKEN, CHAT_ID
from telegram_bot_unittest.routes import TELEGRAM_URL
from main import start_bot
import pytest

pytest_plugins = (
    'telegram_bot_unittest.fixtures',
)


@pytest.fixture(scope='session')
def bot(telegram_server):
    updater = start_bot(BOT_TOKEN, TELEGRAM_URL)
    yield updater.bot
    updater.stop()


user2_id = CHAT_ID+1

u2 = UserBase(user2_id)
chat2 = ChatBase(user2_id)


@pytest.fixture(scope='session')
def user2() -> Tester:
    user2 = Tester(core, u2, chat2)
    return user2
