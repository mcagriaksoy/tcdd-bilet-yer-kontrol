"""
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""

import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


class TelegramMsg:
    """Telegram bot bildirimlerini HTTP API uzerinden yonetir."""

    def __init__(self, timeout=10):
        self.timeout = timeout

    def _request_json(self, endpoint):
        request = Request(endpoint, headers={"User-Agent": "tcdd-bilet-yer-kontrol"})
        with urlopen(request, timeout=self.timeout) as response:
            payload = response.read().decode("utf-8")
        return json.loads(payload)

    def check_telegram_bot_status(self, bot_token):
        """Bot token gecerliligini kontrol eder."""
        if not bot_token:
            return False

        endpoint = f"https://api.telegram.org/bot{bot_token}/getMe"
        try:
            payload = self._request_json(endpoint)
            return bool(payload.get("ok"))
        except (HTTPError, URLError, TimeoutError, ValueError):
            return False

    def send_telegram_message(self, bot_token, chat_id):
        """Telegram uzerinden bilet bulundu mesaji gonderir."""
        message = quote_plus("Hey biletin bulundu! Acele et!")
        endpoint = (
            f"https://api.telegram.org/bot{bot_token}/sendMessage"
            f"?chat_id={chat_id}&text={message}"
        )
        try:
            payload = self._request_json(endpoint)
            return bool(payload.get("ok"))
        except (HTTPError, URLError, TimeoutError, ValueError):
            return False
