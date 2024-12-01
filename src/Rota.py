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


NEREDEN_BOX = "/html/body/div[3]/div[2]/div/div[2]/ul/li[1]/div/form/div[1]/p[4]"
NEREYE_BOX = "/html/body/div[3]/div[2]/div/div[2]/ul/li[1]/div/form/div[2]/p[4]"
TARIH_BOX = ""
BUTTON_BOX = "/html/body/div[3]/div[2]/div/div[2]/ul/li[1]/div/form/div[3]/p[3]/button"

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
            text1 = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#nereden"))
            )
            text1.clear()
            text1.send_keys(self.first_location)
            stdout.write("\nNereden: " + self.first_location)
            sleep(0.2)

            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, NEREDEN_BOX)))
            ActionChains(self.driver).move_to_element(element).perform()
            element.click()

            text2 = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#nereye"))
            )
            text2.clear()
            text2.send_keys(self.last_location)
            stdout.write("\nNereye: " + self.last_location)
            sleep(0.2)

            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, NEREYE_BOX)))
            ActionChains(self.driver).move_to_element(element).perform()
            element.click()
            sleep(0.2)

            date = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#trCalGid_input"))
            )
            date.clear()
            date.send_keys(self.date)
            stdout.write("\nTarih: " + self.date)
            sleep(1)

            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, BUTTON_BOX)))
            self.driver.execute_script("arguments[0].click();", button)

        except UnexpectedAlertPresentException:
            stdout.write(
                "\nGüzergah route bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz."
            )
            return -1
        except TimeoutException:
            stdout.write("\nWebsite Belirlenen surede acilamadi!")
            return -1
