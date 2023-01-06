from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW

class DriverSetting:
    def driverUP(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_service = ChromeService('chromedriver')
        chrome_service.creationflags = CREATE_NO_WINDOW
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options, service=chrome_service)
        
        return driver
