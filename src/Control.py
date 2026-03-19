# -*- coding: utf-8 -*-
"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""

import sys
from time import sleep
import logging
import ctypes
import os

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
    UnexpectedAlertPresentException,
    InvalidSessionIdException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import error_codes as ErrCodes

MAX_TREN_SAYISI = 22


class Control:
    """Class: Sayfada yer var mı yok mu kontrol eder."""

    def __init__(self, driver, time, allow_economy=True, allow_business=False):
        """Constructor methodu."""
        self.driver = driver
        self.zaman = time
        self.allow_economy = allow_economy
        self.allow_business = allow_business
        # logging setup
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

    def kill_driver(self):
        """Driver'ı kapatır."""
        try:
            # Protect against calling methods on a closed/invalid session
            if self.driver:
                session_id = getattr(self.driver, "session_id", None)
                if session_id:
                    try:
                        self.driver.delete_all_cookies()
                    except Exception:
                        self.logger.debug("delete_all_cookies failed or session invalid")
                    try:
                        self.driver.close()
                    except Exception:
                        self.logger.debug("close failed or session invalid")
                    try:
                        self.driver.quit()
                    except Exception:
                        self.logger.debug("quit failed or session invalid")
                else:
                    self.logger.debug("Driver session_id is None or invalid; skipping close/quit.")
            self.logger.info("Driver kapatma işlemi tamamlandı (guarded).")
        except Exception as e:
            self.logger.exception(f"Kill driver sırasında hata: {e}")

    def sayfa_kontrol(self):
        """Sayfada yer var mı yok mu kontrol eder."""
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="seferListScroll"]/div[2]/div/div[1]')
                )
            )
            if element:
                sys.stdout.write("\nAranan saat: " + self.zaman + "\n")
                for row in range(0, MAX_TREN_SAYISI):
                    sleep(0.02)
                    xpath = f'//*[@id="gidis{row}btn"]/div/div[2]/div/div[2]/div[2]/span[1]/time'
                    try:
                        aranan_element = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, xpath))
                        )
                        aranan = aranan_element.text
                    except TimeoutException:
                        sys.stdout.write(
                            f"\nRow {row}: Saat bilgisi alınamadı, atlanıyor..."
                        )
                        continue

                    if self.zaman == aranan:
                        sys.stdout.write("\nAranan saat bulundu...")
                        try:
                            element = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, xpath))
                            )
                            element.click()
                        except (TimeoutException, ElementClickInterceptedException):
                            sys.stdout.write(
                                "\nSaat seçimi sırasında hata oluştu, tekrar denenecek!"
                            )
                            return ErrCodes.TEKRAR_DENE

                        business_row, economy_row = 0, 0
                        for index in range(1, 5):
                            try:
                                text = (
                                    WebDriverWait(self.driver, 10)
                                    .until(
                                        EC.visibility_of_element_located(
                                            (
                                                By.XPATH,
                                                f"html/body/div/main/section/div[2]/div/div[1]/div/div/section/div[{row + 1}]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[{index}]/button/div/div[1]/span",
                                            )
                                        )
                                    )
                                    .text
                                )
                                print(f"Index: {index}, Text: {text}")
                                if text == "EKONOMİ":
                                    economy_row = index
                                elif text == "BUSİNESS":
                                    business_row = index
                            except TimeoutException:
                                print(f"Index {index} not found, skipping...")

                        if economy_row == 0:
                            sys.stdout.write(
                                "\nAradığınız seferde ekonomi ya da business koltuğu bulunamadı!"
                            )
                            return ErrCodes.TEKRAR_DENE

                        print(
                            f"Economy Row: {economy_row}, Business Row: {business_row}"
                        )

                        economy_seat = None
                        business_seat = None
                        try:
                            if economy_row:
                                economy_seat = (
                                    WebDriverWait(self.driver, 10)
                                    .until(
                                        EC.visibility_of_element_located(
                                            (
                                                By.XPATH,
                                                f"/html/body/div/main/section/div[2]/div/div[1]/div/div/section/div[{row + 1}]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[{economy_row}]/button/div/div[2]/div/div/span",
                                            )
                                        )
                                    )
                                    .text
                                )
                            if business_row:
                                business_seat = (
                                    WebDriverWait(self.driver, 10)
                                    .until(
                                        EC.visibility_of_element_located(
                                            (
                                                By.XPATH,
                                                f"/html/body/div/main/section/div[2]/div/div[1]/div/div/section/div[{row + 1}]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[{business_row}]/button/div/div[2]/div/div/span",
                                            )
                                        )
                                    )
                                    .text
                                )
                        except TimeoutException:
                            sys.stdout.write(
                                "\nKoltuk bilgisi alınamadı, tekrar denenecek!"
                            )
                            return ErrCodes.TEKRAR_DENE

                        print(
                            f"Economy Seat: {economy_seat}, Business Seat: {business_seat}"
                        )

                        try:
                            economy_seat = (
                                int(economy_seat[1:-1]) if economy_seat else 0
                            )
                            business_seat = (
                                int(business_seat[1:-1]) if business_seat else 0
                            )
                        except ValueError:
                            sys.stdout.write(
                                "\nKoltuk bilgisi dönüştürülemedi, tekrar denenecek!"
                            )
                            return ErrCodes.TEKRAR_DENE

                        economy_match = self.allow_economy and economy_seat > 0
                        business_match = self.allow_business and business_seat > 0

                        if economy_match and economy_seat > 2:
                            sys.stdout.write("\nEkonomi sinifinda yeteri kadar bos yer mevcut!")
                            return ErrCodes.BASARILI
                        if business_match and business_seat > 2:
                            sys.stdout.write("\nBusiness sinifinda yeteri kadar bos yer mevcut!")
                            return ErrCodes.BASARILI
                        if economy_match and economy_seat in [1, 2]:
                            sys.stdout.write(
                                f"\nEKONOMI SINIFINDA bos koltuk sayisi: {economy_seat}. Acele et!"
                            )
                            return ErrCodes.BASARILI
                        if business_match and business_seat in [1, 2]:
                            sys.stdout.write(
                                f"\nBUSINESS SINIFINDA bos koltuk sayisi: {business_seat}. Acele et!"
                            )
                            return ErrCodes.BASARILI

                        sys.stdout.write(
                            "\nSecilen bilet tipinde uygun bos yer bulunamadi."
                        )
                        return ErrCodes.TEKRAR_DENE

                self.kill_driver()
                return ErrCodes.SAAT_HATASI
            else:
                sys.stdout.write("\nAradığınız seferde boş yer yoktur...")
                self.kill_driver()
                return ErrCodes.TEKRAR_DENE
        except InvalidSessionIdException as ise:
            # Browser/session closed unexpectedly -> log, notify, cleanup and return retry
            msg = f"Tarayıcı oturumu geçersiz: {ise}"
            sys.stdout.write("\n" + msg)
            self.logger.exception(msg)
            try:
                self.kill_driver()
            except Exception:
                self.logger.debug("kill_driver failed after InvalidSessionIdException")
            self._notify_user("Tarayıcı oturumu kapandı veya bağlantı koptu.", "Oturum Koptu")
            return ErrCodes.TIMEOUT_HATASI
        except TimeoutException:
            msg = "Zaman aşımına uğradı..."
            sys.stdout.write("\n" + msg)
            self.logger.exception(msg)
            try:
                self.kill_driver()
            except Exception:
                self.logger.debug("kill_driver failed after TimeoutException")
            self._notify_user(msg, "Timeout Hatası")
            return ErrCodes.TIMEOUT_HATASI
        except NoSuchElementException:
            msg = "Aranan saat ya da sefer bulunamadı..."
            sys.stdout.write("\n" + msg)
            self.logger.exception(msg)
            try:
                self.kill_driver()
            except Exception:
                self.logger.debug("kill_driver failed after NoSuchElementException")
            self._notify_user(msg, "Element Bulunamadı")
            return ErrCodes.TEKRAR_DENE
        except UnexpectedAlertPresentException:
            msg = "Güzergah bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz."
            sys.stdout.write("\n" + msg)
            self.logger.exception(msg)
            try:
                self.kill_driver()
            except Exception:
                self.logger.debug("kill_driver failed after UnexpectedAlertPresentException")
            self._notify_user(msg, "Güzergah Hatası")
            return ErrCodes.GUZERGAH_HATASI
        except ConnectionAbortedError:
            self.kill_driver()
            self.driver.quit()
            return ErrCodes.INTERNET_HATASI
        except ConnectionResetError:
            self.kill_driver()
            self.driver.quit()
            return ErrCodes.INTERNET_HATASI
        except Exception as e:
            msg = f"Bilinmeyen bir hata oluştu: {e}"
            sys.stdout.write("\n" + msg)
            self.logger.exception(msg)
            try:
                self.kill_driver()
                self.driver.quit()
            except Exception:
                self.logger.debug("kill_driver failed after generic exception")
            self._notify_user(msg, "Bilinmeyen Hata")
            return ErrCodes.TEKRAR_DENE
