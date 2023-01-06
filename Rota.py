"""
@author: Birol Emekli, Mehmet Çağrı Aksoy
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import UnexpectedAlertPresentException
import sys
import time
class Rota:
    def __init__(self,driver,nereden,nereye,date):
        self.driver=driver
        self.first_location=nereden
        self.last_location=nereye
        self.date=date

    def dataInput(self):
        try:

            text1 = self.driver.find_element(By.CSS_SELECTOR ,"#nereden")
            text1.clear()
            text1.send_keys(self.first_location)
            sys.stdout.write('\nNereden: ' + self.first_location)
            time.sleep(0.5)

            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ul[1]/li/a")))
            ActionChains(self.driver).move_to_element(element).perform()
            element.click()
            
            text2 = self.driver.find_element(By.CSS_SELECTOR ,"#nereye")
            text2.clear()
            text2.send_keys(self.last_location)
            sys.stdout.write('\nNereye: ' + self.last_location)            
            time.sleep(0.5)

            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ul[2]/li/a")))
            ActionChains(self.driver).move_to_element(element).perform()
            element.click()
            time.sleep(0.5)

            date = self.driver.find_element(By.CSS_SELECTOR ,"#trCalGid_input")
            date.clear()
            date.send_keys(self.date)
            sys.stdout.write('\nTarih: '+self.date)
            time.sleep(0.5)
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/ul/li[1]/div/form/div[3]/p[3]/button/span")))
            self.driver.execute_script("arguments[0].click();", button)
            
        except:
            sys.stdout.write("\nGüzergah bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz. İstasyonları doğru girdiğinizden emin olunuz")
            self.driver.quit()
            exit()
