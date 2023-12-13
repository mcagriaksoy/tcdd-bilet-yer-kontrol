"""
@author: Mehmet Çağrı Aksoy
"""
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class DriverSetting:
    ''' Driver'ı ayarlar.'''

    def driver_init(self):
        ''' Driver'ı ayarlar.'''
        options = webdriver.ChromeOptions()
        # chrome_options.headless = False
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=320,480')
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        try:
            driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=options)
        except:
            time.sleep(1)  # 1 saniye bekle!
            driver = webdriver.Chrome(options=options)

        return driver
