"""
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""

from telegram import Bot

class TelegramMsg:
    """ Send a message to your Telegram bot when the event occurs. """

    def __init__(self):
        pass

    def check_telegram_bot_status(self, bot_token):
        ''' Check the status of your Telegram bot. '''
        try:
            bot = Bot(token=bot_token)
            bot.get_me()
            return True
        except Exception as e:
            print(f"Error checking Telegram bot status: {e}")
            return False

    def send_telegram_message(self, bot_token, chat_id):
        ''' Send a message to your Telegram bot when the event occurs.'''
        bot = Bot(token=bot_token)
        try:
            bot = Bot(token=bot_token)
            bot.send_message(chat_id=chat_id, text="Hey biletin bulundu! Acele et!")
        except TelegramError as e:
            print(f"Error sending Telegram message: {e}")
