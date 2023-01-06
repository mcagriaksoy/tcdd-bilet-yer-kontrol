"""
@author: Mehmet Çağrı Aksoy
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class DriverSetting:
    def driverUP(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=640,480')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        return driver
