"""
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""

from telegram import Bot


class TelegramMsg:
    """ Send a message to your Telegram bot when the event occurs. """

    def __init__(self):
        pass

    def save_telegram_settings(self, bot_token, chat_id):
        ''' Save your Telegram bot token and chat id to a file.'''
        with open("telegram_settings.txt", "w") as f:
            f.write(bot_token + "\n")
            f.write(chat_id)

    def send_telegram_message(self, bot_token, chat_id):
        ''' Send a message to your Telegram bot when the event occurs.'''
        bot = Bot(token=bot_token)

        if event:
            bot.send_message(
                chat_id=chat_id, text="Hey biletin bulundu! Acele et!")
