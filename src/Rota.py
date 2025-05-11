"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""

from sys import stdout
from time import sleep

from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

NEREDEN_BOX = "//*[@id=\"fromTrainInput\"]"
NEREYE_BOX = "//*[@id=\"toTrainInput\"]"
TARIH_BOX = "//*[@id=\"__BVID__101\"]/section/div[3]"
BUTTON_BOX = "//*[@id=\"searchSeferButton\"]"
DATE_TODAY = '#__BVID__101 > section > div.row.pb-3.seferSearchDateRangePicker > div > div > div.daterangepicker.ltr.show-calendar.single.openscenter.linked > div.calendars > div > div.drp-calendar.col.left.single > div > table > tbody > tr:nth-child(4) > td.weekend.today.start-date'

class Rota:
    """Rota bilgilerini alır ve gerekli yerlere yazar."""

    def __init__(self, driver, nereden, nereye, date):
        self.driver = driver
        self.first_location = nereden
        self.last_location = nereye
        self.date = date

    def dataInput(self):
        """Rota bilgilerini alır ve gerekli yerlere yazar."""
        try:
            element = WebDriverWait(self.driver, 22).until(EC.visibility_of_element_located((By.XPATH, NEREDEN_BOX)))
            ActionChains(self.driver).move_to_element(element).perform()
            element.click()

            element.send_keys(self.first_location)

            # Wait for the dynamic element to be clickable and click it
            dynamic_element = WebDriverWait(self.driver, 22).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'gidis-')]"))
            )
            dynamic_element.click()

######################################################################################
            sleep(1)

            element2 = WebDriverWait(self.driver, 22).until(EC.visibility_of_element_located((By.XPATH, NEREYE_BOX)))
            ActionChains(self.driver).move_to_element(element2).perform()
            element2.click()

            element2.send_keys(self.last_location)

            # Wait for the dynamic element to be clickable and click it
            dynamic_element = WebDriverWait(self.driver, 22).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'donus-')]"))
            )
            dynamic_element.click()
######################################################################################
            sleep(1)

            element3 = WebDriverWait(self.driver, 22).until(EC.visibility_of_element_located((By.XPATH, TARIH_BOX)))
            ActionChains(self.driver).move_to_element(element3).perform()
            element3.click()
            
            # IF DATE IS TODAY use specific CSS_SELECTOR
            if self.date == 'bugün':
                dynamic_element = WebDriverWait(self.driver, 22).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, DATE_TODAY))
                )
                dynamic_element.click()
            else:
                date_splitted = self.date.split('.')
                day = date_splitted[0]
                month = date_splitted[1]
                year = date_splitted[2]

                new_xpath = f'//*[@id="{day} {month} {year}"]'

                dynamic_element = WebDriverWait(self.driver, 22).until(
                    EC.element_to_be_clickable((By.XPATH, new_xpath)))
                dynamic_element.click()

######################################################################################
            sleep(1)
            element4 = WebDriverWait(self.driver, 22).until(EC.visibility_of_element_located((By.XPATH, BUTTON_BOX)))
            element4.click()


        except UnexpectedAlertPresentException:
            stdout.write(
                "\nGüzergah route bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz."
            )
            return -1
        except TimeoutException:
            stdout.write("\nWebsite Belirlenen surede acilamadi!")
            return -1
