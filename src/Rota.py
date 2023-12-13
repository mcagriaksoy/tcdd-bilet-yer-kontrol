"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""

import sys
import time

from selenium.common.exceptions import (TimeoutException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Rota:
    ''' Rota bilgilerini alır ve gerekli yerlere yazar. '''

    def __init__(self, driver, nereden, nereye, date):
        self.driver = driver
        self.first_location = nereden
        self.last_location = nereye
        self.date = date

    def dataInput(self):
        ''' Rota bilgilerini alır ve gerekli yerlere yazar.'''
        try:
            text1 = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#nereden")))
            text1.clear()
            text1.send_keys(self.first_location)
            sys.stdout.write('\nNereden: ' + self.first_location)
            time.sleep(0.2)

            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/ul/li[1]/div/form/div[1]/p[4]")))
            ActionChains(self.driver).move_to_element(element).perform()
            element.click()

            text2 = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#nereye")))
            text2.clear()
            text2.send_keys(self.last_location)
            sys.stdout.write('\nNereye: ' + self.last_location)
            time.sleep(0.2)

            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/ul/li[1]/div/form/div[1]/p[6]/span/input")))
            ActionChains(self.driver).move_to_element(element).perform()
            element.click()
            time.sleep(0.2)

            date = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#trCalGid_input")))
            date.clear()
            date.send_keys(self.date)
            sys.stdout.write('\nTarih: ' + self.date)
            time.sleep(0.2)

            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/ul/li[1]/div/form/div[3]/p[3]/button")))
            self.driver.execute_script("arguments[0].click();", button)

        except UnexpectedAlertPresentException:
            sys.stdout.write(
                "\nGüzergah route bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz.")
            return -1
        except TimeoutException:
            sys.stdout.write("\nWebsite Belirlenen surede acilamadi!")
            return -1
