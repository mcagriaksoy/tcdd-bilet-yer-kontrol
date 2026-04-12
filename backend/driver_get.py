"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Cagri Aksoy https://github.com/mcagriaksoy
"""

import ctypes
import logging
import os
import sys

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    InvalidSessionIdException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TCDD_POPUP_CLOSE_BUTTON_XPATH = "/html/body/div[2]/div[1]/div/div/header/div/button"


class DriverGet:
    """Gets driver and loads page."""

    def __init__(self, driver, url="https://ebilet.tcddtasimacilik.gov.tr", logger=None):
        if driver is None:
            raise ValueError("Driver cannot be None")
        self.url = url
        self.driver = driver
        if logger is not None:
            self.logger = logger
        elif not logging.getLogger().handlers:
            logging.basicConfig(
                filename=os.path.join(os.getcwd(), "tcdd_debug.log"),
                level=logging.DEBUG,
                format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                encoding="utf-8",
            )
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logging.getLogger(__name__)

    def _notify_user(self, message, title="TCDD Bilet"):
        try:
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
        except Exception:
            self.logger.debug("Popup failed")

    def _enforce_window_geometry(self):
        try:
            self.driver.set_window_rect(x=0, y=0, width=640, height=480)
            rect = self.driver.get_window_rect()
            self.logger.info(
                "DriverGet pencere boyutu: "
                f"{rect.get('width')}x{rect.get('height')} @ "
                f"({rect.get('x')},{rect.get('y')})"
            )
        except Exception as exc:
            self.logger.debug(f"DriverGet pencere boyutu ayarlanamadi: {exc}")

    def _close_tcdd_popup_if_visible(self):
        try:
            close_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, TCDD_POPUP_CLOSE_BUTTON_XPATH))
            )
            try:
                close_button.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", close_button)
            self.logger.info("TCDD popup kapatildi.")
        except TimeoutException:
            self.logger.debug("TCDD popup gorunmuyor, devam ediliyor.")
        except Exception as exc:
            self.logger.debug(f"TCDD popup kapatilamadi: {exc}")

    def driver_get(self):
        """Loads page with guarded session handling."""
        try:
            self._enforce_window_geometry()
            self.driver.get(self.url)
            self._enforce_window_geometry()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "body > div > main > section.homePageSearchArea > div > div > div",
                    )
                )
            )
            self._close_tcdd_popup_if_visible()
            sys.stdout.write("Sayfa yuklendi...")
            self.logger.info(f"Sayfa yuklendi: {self.url}")
        except InvalidSessionIdException as ise:
            self.logger.exception(f"InvalidSessionIdException sayfa yuklenirken: {ise}")
            self._notify_user(
                "Tarayici oturumu gecersiz hale geldi (InvalidSessionId). "
                "Tarayici tekrar baslatilacak.",
                "Oturum Hatasi",
            )
            raise
        except Exception as exc:
            self.logger.exception(f"Sayfa yuklenirken hata olustu: {exc}")
            self._notify_user(f"Sayfa yuklenemedi: {exc}", "Sayfa Yukleme Hatasi")
            raise
