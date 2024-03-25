"""
@author: Mehmet Çağrı Aksoy
"""

import time

from selenium.webdriver import ChromeOptions, Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class DriverSetting:
    """Driver'ı ayarlar."""

    def driver_init(self):
        """Driver'ı ayarlar."""
        options = ChromeOptions()
        # chrome_options.headless = False
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=320,480")
        # options.add_argument('--headless')
        options.add_argument("--disable-gpu")
        # options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        try:
            driver = Chrome(ChromeDriverManager().install(), options=options)
        except:
            time.sleep(1)  # 1 saniye bekle!
            driver = Chrome(options=options)

        return driver
