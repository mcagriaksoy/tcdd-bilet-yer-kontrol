"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""

from sys import stdout
from datetime import date
from time import sleep

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

NEREDEN_BOX = '//*[@id="fromTrainInput"]'
NEREYE_BOX = '//*[@id="toTrainInput"]'
BUTTON_BOX = '//*[@id="searchSeferButton"]'


class Rota:
    """Rota bilgilerini alır ve gerekli yerlere yazar."""

    def __init__(self, driver, nereden, nereye, date):
        self.driver = driver
        self.first_location = nereden
        self.last_location = nereye
        self.date = date
        self.short_wait = WebDriverWait(self.driver, 1.0)
        self.medium_wait = WebDriverWait(self.driver, 5)

    def _safe_click(self, element):
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def _click_date_box(self):
        selectors = [
            (By.XPATH, '//*[@id="gidisTarih"]'),
            (By.XPATH, '//*[@id="departureDate"]'),
            (By.XPATH, '//input[contains(@class, "datepicker")]'),
            (By.XPATH, '//input[contains(@name, "departure")]'),
            (By.XPATH, '//input[contains(@placeholder, "Tarih")]'),
            (By.XPATH, '//div[contains(@class, "date")]//input'),
            (By.XPATH, '//section//div[contains(@class, "datepicker")]'),
            (By.XPATH, '//div[contains(@class, "daterange")]'),
            (By.XPATH, '//span[contains(text(), "Tarih")]/ancestor::div[1]'),
        ]

        last_error = None
        for by, selector in selectors:
            try:
                elements = self.driver.find_elements(by, selector)
                if not elements:
                    continue
                element = elements[0]
                ActionChains(self.driver).move_to_element(element).pause(0.2).perform()
                self._safe_click(element)
                self.short_wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            '//div[contains(@class, "daterangepicker") and contains(@style, "display: block")]'
                            '|//div[contains(@class, "daterangepicker") and contains(@class, "show-calendar")]'
                            '|//table[contains(@class, "table-condensed")]',
                        )
                    )
                )
                return True
            except Exception as exc:
                last_error = exc
        raise TimeoutException(f"Tarih kutusu açılamadı: {last_error}")

    def _select_date(self):
        day, month, year = self.date.split(".")
        day = str(int(day))

        selectors = [
            (
                By.XPATH,
                f'//*[@id="{day.zfill(2)} {month} {year}" or @id="{day} {month} {year}"]',
            ),
            (
                By.XPATH,
                f'//td[normalize-space()="{day}" and not(contains(@class, "off")) and not(contains(@class, "disabled"))]',
            ),
            (
                By.XPATH,
                f'//button[normalize-space()="{day}" and not(@disabled)]',
            ),
            (
                By.XPATH,
                f'//*[@aria-label="{self.date}"]',
            ),
        ]

        last_error = None
        for by, selector in selectors:
            try:
                element = self.short_wait.until(
                    EC.element_to_be_clickable((by, selector))
                )
                self._safe_click(element)
                return True
            except Exception as exc:
                last_error = exc
        raise TimeoutException(f"Tarih seçilemedi: {last_error}")

    def _is_today_selected(self):
        return self.date == date.today().strftime("%d.%m.%Y")

    def dataInput(self):
        """Rota bilgilerini alır ve gerekli yerlere yazar."""
        try:
            element = WebDriverWait(self.driver, 12).until(
                EC.visibility_of_element_located((By.XPATH, NEREDEN_BOX))
            )
            ActionChains(self.driver).move_to_element(element).perform()
            self._safe_click(element)
            element.send_keys(self.first_location)

            dynamic_element = self.medium_wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'gidis-')]"))
            )
            self._safe_click(dynamic_element)

            sleep(0.25)

            element2 = WebDriverWait(self.driver, 12).until(
                EC.visibility_of_element_located((By.XPATH, NEREYE_BOX))
            )
            ActionChains(self.driver).move_to_element(element2).perform()
            self._safe_click(element2)
            element2.send_keys(self.last_location)

            dynamic_element = self.medium_wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'donus-')]"))
            )
            self._safe_click(dynamic_element)

            sleep(0.2)
            if not self._is_today_selected():
                self._click_date_box()
                sleep(0.15)
                self._select_date()

            sleep(0.2)
            element4 = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, BUTTON_BOX))
            )
            self._safe_click(element4)

        except UnexpectedAlertPresentException:
            stdout.write(
                "\nGüzergah route bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz."
            )
            return -1
        except (TimeoutException, ElementClickInterceptedException) as exc:
            stdout.write(f"\nTarih veya güzergah seçimi yapılamadı: {exc}")
            return -1
