# -*- coding: utf-8 -*-
"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Ã‡aÄŸrÄ± Aksoy https://github.com/mcagriaksoy
"""

import sys
import re
from time import sleep, monotonic
import logging
import ctypes
import os

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    UnexpectedAlertPresentException,
    InvalidSessionIdException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from . import error_codes as ErrCodes
from .driver_setting import resolve_logs_dir

MAX_TREN_SAYISI = 22


class Control:
    """Class: Sayfada yer var mÄ± yok mu kontrol eder."""

    def __init__(
        self,
        driver,
        time,
        allow_economy=True,
        allow_business=False,
        logger=None,
        stop_event=None,
    ):
        """Constructor methodu."""
        self.driver = driver
        self.zaman = time
        self.allow_economy = allow_economy
        self.allow_business = allow_business
        self.stop_event = stop_event
        # logging setup
        if logger is not None:
            self.logger = logger
        elif not logging.getLogger().handlers:
            logging.basicConfig(
                filename=os.path.join(resolve_logs_dir(), "tcdd_debug.log"),
                level=logging.DEBUG,
                format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                encoding="utf-8",
            )
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logging.getLogger(__name__)

    def _is_stop_requested(self):
        return bool(self.stop_event and self.stop_event.is_set())

    @staticmethod
    def _normalize_label(text):
        raw = (text or "").strip().upper()
        replacements = {
            "Ä°": "I",
            "İ": "I",
            "İ": "I",
            "Ş": "S",
            "Ğ": "G",
            "Ü": "U",
            "Ö": "O",
            "Ç": "C",
            "Â": "A",
        }
        for source, target in replacements.items():
            raw = raw.replace(source, target)
        return raw

    def _notify_user(self, message, title="TCDD Bilet"):
        try:
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
        except Exception:
            self.logger.debug("Popup failed")

    def _available_train_rows(self):
        rows = []
        elements = self.driver.find_elements(
            By.XPATH, "//*[starts-with(@id, 'gidis') and contains(@id, 'btn')]"
        )
        for element in elements:
            element_id = (element.get_attribute("id") or "").strip()
            match = re.fullmatch(r"gidis(\d+)btn", element_id)
            if match:
                rows.append(int(match.group(1)))
        return sorted(set(rows))

    def _wait_for_available_train_rows(self, timeout=20):
        deadline = monotonic() + timeout
        last_rows = []
        stable_hits = 0

        while monotonic() < deadline:
            rows = self._available_train_rows()
            if rows:
                if rows == last_rows:
                    stable_hits += 1
                else:
                    stable_hits = 1
                    last_rows = rows
                if stable_hits >= 2:
                    return rows
            else:
                stable_hits = 0
                last_rows = []
            sleep(0.4)

        return last_rows

    def kill_driver(self):
        """Driver'Ä± kapatÄ±r."""
        try:
            # Protect against calling methods on a closed/invalid session
            if self.driver:
                if getattr(self.driver, "_tcdd_cleanup_done", False):
                    self.driver = None
                    return
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
                try:
                    setattr(self.driver, "_tcdd_cleanup_done", True)
                except Exception:
                    pass
                self.driver = None
            self.logger.info("Driver kapatma iÅŸlemi tamamlandÄ± (guarded).")
        except Exception as e:
            self.logger.exception(f"Kill driver sÄ±rasÄ±nda hata: {e}")

    def sayfa_kontrol(self):
        """Sayfada yer var mÄ± yok mu kontrol eder."""
        try:
            WebDriverWait(self.driver, 8).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="seferListScroll"]')
                )
            )
            rows = self._wait_for_available_train_rows(timeout=20)
            self.logger.info("Mevcut sefer satirlari: %s", rows)
            if rows:
                sys.stdout.write("\nAranan saat: " + self.zaman + "\n")
                for row in rows:
                    xpath = f'//*[@id="gidis{row}btn"]/div/div[2]/div/div[2]/div[2]/span[1]/time'
                    try:
                        candidates = self.driver.find_elements(By.XPATH, xpath)
                        aranan_element = candidates[0] if candidates else None
                        if aranan_element is None:
                            sys.stdout.write(
                                f"\nRow {row}: Saat elementi bos geldi, atlaniyor..."
                            )
                            continue
                        aranan = (aranan_element.text or "").strip()
                        self.logger.info(
                            "Sefer satiri okundu: row=%s saat=%s hedef=%s",
                            row,
                            aranan,
                            self.zaman,
                        )
                    except (
                        TimeoutException,
                        AttributeError,
                        StaleElementReferenceException,
                    ):
                        sys.stdout.write(
                            f"\nRow {row}: Saat bilgisi alÄ±namadÄ±, atlanÄ±yor..."
                        )
                        continue

                    if self.zaman == aranan:
                        sys.stdout.write("\nAranan saat bulundu...")
                        try:
                            element = WebDriverWait(self.driver, 4).until(
                                EC.element_to_be_clickable((By.XPATH, xpath))
                            )
                            element.click()
                        except (TimeoutException, ElementClickInterceptedException):
                            sys.stdout.write(
                                "\nSaat seÃ§imi sÄ±rasÄ±nda hata oluÅŸtu, tekrar denenecek!"
                            )
                            return ErrCodes.TEKRAR_DENE

                        business_row, economy_row = 0, 0
                        for index in range(1, 5):
                            try:
                                text = (
                                    WebDriverWait(self.driver, 4)
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
                                normalized_text = self._normalize_label(text)
                                self.logger.info(
                                    "Kabin tipi metni: row=%s index=%s raw=%s normalized=%s",
                                    row,
                                    index,
                                    text,
                                    normalized_text,
                                )
                                if "EKONOM" in normalized_text:
                                    economy_row = index
                                elif "BUSINESS" in normalized_text:
                                    business_row = index
                            except (
                                TimeoutException,
                                AttributeError,
                                StaleElementReferenceException,
                            ):
                                print(f"Index {index} not found, skipping...")
                                self.logger.info(
                                    "Kabin tipi okunamadi: row=%s index=%s",
                                    row,
                                    index,
                                )

                        self.logger.info(
                            "Kabin tipi satirlari: row=%s economy_row=%s business_row=%s",
                            row,
                            economy_row,
                            business_row,
                        )

                        if economy_row == 0:
                            sys.stdout.write(
                                "\nAradÄ±ÄŸÄ±nÄ±z seferde ekonomi ya da business koltuÄŸu bulunamadÄ±!"
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
                                    WebDriverWait(self.driver, 4)
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
                                    WebDriverWait(self.driver, 4)
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
                        except (
                            TimeoutException,
                            AttributeError,
                            StaleElementReferenceException,
                        ):
                            sys.stdout.write(
                                "\nKoltuk bilgisi alÄ±namadÄ±, tekrar denenecek!"
                            )
                            return ErrCodes.TEKRAR_DENE

                        self.logger.info(
                            "Koltuk metinleri: row=%s economy_text=%s business_text=%s",
                            row,
                            economy_seat,
                            business_seat,
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
                                "\nKoltuk bilgisi dÃ¶nÃ¼ÅŸtÃ¼rÃ¼lemedi, tekrar denenecek!"
                            )
                            return ErrCodes.TEKRAR_DENE

                        self.logger.info(
                            "Koltuk sayilari: row=%s economy=%s business=%s allow_economy=%s allow_business=%s",
                            row,
                            economy_seat,
                            business_seat,
                            self.allow_economy,
                            self.allow_business,
                        )

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
                self.logger.info(
                    "Hedef saat bulunamadi: hedef=%s allow_economy=%s allow_business=%s",
                    self.zaman,
                    self.allow_economy,
                    self.allow_business,
                )
                return ErrCodes.SAAT_HATASI
            else:
                sys.stdout.write(
                    "\nSefer listesi zamaninda yuklenemedi, tekrar denenecek."
                )
                self.logger.warning(
                    "Sefer listesi yuklenemedi veya satirlar hazir olmadan kontrol tamamlandi."
                )
                self.kill_driver()
                return ErrCodes.TEKRAR_DENE
        except InvalidSessionIdException as ise:
            # Browser/session closed unexpectedly -> log, notify, cleanup and return retry
            msg = f"TarayÄ±cÄ± oturumu geÃ§ersiz: {ise}"
            sys.stdout.write("\n" + msg)
            self.logger.exception(msg)
            try:
                self.kill_driver()
            except Exception:
                self.logger.debug("kill_driver failed after InvalidSessionIdException")
            if not self._is_stop_requested():
                self._notify_user("TarayÄ±cÄ± oturumu kapandÄ± veya baÄŸlantÄ± koptu.", "Oturum Koptu")
            return ErrCodes.TIMEOUT_HATASI
        except TimeoutException:
            msg = "Zaman aÅŸÄ±mÄ±na uÄŸradÄ±..."
            sys.stdout.write("\n" + msg)
            self.logger.exception(msg)
            try:
                self.kill_driver()
            except Exception:
                self.logger.debug("kill_driver failed after TimeoutException")
            if not self._is_stop_requested():
                self._notify_user(msg, "Timeout HatasÄ±")
            return ErrCodes.TIMEOUT_HATASI
        except NoSuchElementException:
            msg = "Aranan saat ya da sefer bulunamadÄ±..."
            sys.stdout.write("\n" + msg)
            self.logger.exception(msg)
            try:
                self.kill_driver()
            except Exception:
                self.logger.debug("kill_driver failed after NoSuchElementException")
            if not self._is_stop_requested():
                self._notify_user(msg, "Element BulunamadÄ±")
            return ErrCodes.TEKRAR_DENE
        except UnexpectedAlertPresentException:
            msg = "GÃ¼zergah bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz."
            sys.stdout.write("\n" + msg)
            self.logger.exception(msg)
            try:
                self.kill_driver()
            except Exception:
                self.logger.debug("kill_driver failed after UnexpectedAlertPresentException")
            if not self._is_stop_requested():
                self._notify_user(msg, "GÃ¼zergah HatasÄ±")
            return ErrCodes.GUZERGAH_HATASI
        except ConnectionAbortedError:
            self.kill_driver()
            return ErrCodes.INTERNET_HATASI
        except ConnectionResetError:
            self.kill_driver()
            return ErrCodes.INTERNET_HATASI
        except Exception as e:
            if "is_displayed" in str(e):
                msg = "Saat satiri okunamadi, sefer saati bulunamadi kabul edildi."
                sys.stdout.write("\n" + msg)
                self.logger.exception(msg)
                try:
                    self.kill_driver()
                except Exception:
                    self.logger.debug("kill_driver failed after is_displayed error")
                return ErrCodes.SAAT_HATASI
            msg = f"Bilinmeyen bir hata oluÅŸtu: {e}"
            sys.stdout.write("\n" + msg)
            self.logger.exception(msg)
            try:
                self.kill_driver()
            except Exception:
                self.logger.debug("kill_driver failed after generic exception")
            if not self._is_stop_requested():
                self._notify_user(msg, "Bilinmeyen Hata")
            return ErrCodes.TEKRAR_DENE

