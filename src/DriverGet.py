"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""

import sys
import logging
import ctypes
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import InvalidSessionIdException


class DriverGet:
    """Driver'ı alır ve sayfayı yükler."""

    def __init__(self, driver, url="https://ebilet.tcddtasimacilik.gov.tr"):
        if driver is None:
            raise ValueError("Driver cannot be None")
        self.url = url
        self.driver = driver
        # logging setup if not already configured
        if not logging.getLogger().handlers:
            logging.basicConfig(
                filename=os.path.join(os.getcwd(), "tcdd_debug.log"),
                level=logging.DEBUG,
                format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            )
        self.logger = logging.getLogger(__name__)

    def _notify_user(self, message, title="TCDD Bilet"):
        try:
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
        except Exception:
            self.logger.debug("Popup failed")

    def driver_get(self):
        """Driver'ı alır ve sayfayı yükler."""
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "body > div > main > section.homePageSearchArea > div > div > div",
                    )
                )
            )
            sys.stdout.write("Sayfa yüklendi...")
            self.logger.info(f"Sayfa yüklendi: {self.url}")
        except InvalidSessionIdException as ise:
            # Specific handling for invalid session (browser closed/disconnected)
            self.logger.exception(f"InvalidSessionIdException sayfa yüklenirken: {ise}")
            self._notify_user("Tarayıcı oturumu geçersiz hale geldi (InvalidSessionId). Tarayıcı tekrar başlatılacak.", "Oturum Hatası")
            raise
        except Exception as e:
            self.logger.exception(f"Sayfa yüklenirken hata oluştu: {e}")
            self._notify_user(f"Sayfa yüklenemedi: {e}", "Sayfa Yükleme Hatası")
            raise
