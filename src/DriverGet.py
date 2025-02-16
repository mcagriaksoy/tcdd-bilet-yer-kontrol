"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""

import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class DriverGet:
    ''' Driver'ı alır ve sayfayı yükler.'''

    def __init__(self, driver, url="https://ebilet.tcddtasimacilik.gov.tr"):
        if driver is None:
            raise ValueError("Driver cannot be None")
        self.url = url
        self.driver = driver

    def driver_get(self):
        ''' Driver'ı alır ve sayfayı yükler.'''
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "body > div > main > section.homePageSearchArea > div > div > div")))
        sys.stdout.write("Sayfa yüklendi...")
