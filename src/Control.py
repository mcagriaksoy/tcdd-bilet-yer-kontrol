# -*- coding: utf-8 -*-
"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""
import sys
from time import sleep
from re import search
import error_codes as ErrCodes
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException,
                                        ElementClickInterceptedException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

MAX_TREN_SAYISI = 22

class Control:
    ''' Class: Sayfada yer var mı yok mu kontrol eder.'''

    def __init__(self, driver, time):
        ''' Constructor methodu.'''
        self.driver = driver
        self.zaman = time

    def kill_driver(self):
        ''' Driver'ı kapatır.'''
        self.driver.delete_all_cookies()
        self.driver.close()
        self.driver.quit()

    def sayfa_kontrol(self):
        ''' Sayfada yer var mı yok mu kontrol eder.'''
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="seferListScroll"]/div[2]/div/div[1]')))
            if element:
                sys.stdout.write("\nAranan saat: " + self.zaman + "\n")
                for row in range(0, MAX_TREN_SAYISI):
                    sleep(0.2)
                    xpath = f'//*[@id="gidis{row}btn"]/div/div[2]/div/div[2]/div[2]/span[1]/time'
                    try:
                        aranan_element = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, xpath)))
                        aranan = aranan_element.text
                    except TimeoutException:
                        sys.stdout.write(f"\nRow {row}: Saat bilgisi alınamadı, atlanıyor...")
                        continue

                    if self.zaman == aranan:
                        sys.stdout.write("\nAranan saat bulundu...")
                        try:
                            element = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, xpath)))
                            element.click()
                        except (TimeoutException, ElementClickInterceptedException):
                            sys.stdout.write("\nSaat seçimi sırasında hata oluştu, tekrar denenecek!")
                            return ErrCodes.TEKRAR_DENE

                        business_row, economy_row = 0, 0
                        for index in range(1, 5):
                            try:
                                text = WebDriverWait(self.driver, 10).until(
                                    EC.visibility_of_element_located(
                                        (By.XPATH, f'html/body/div/main/section/div[2]/div/div[1]/div/div/section/div[{row+1}]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[{index}]/button/div/div[1]/span'))).text
                                print(f"Index: {index}, Text: {text}")
                                if text == "EKONOMİ":
                                    economy_row = index
                                elif text == "BUSİNESS":
                                    business_row = index
                            except TimeoutException:
                                print(f"Index {index} not found, skipping...")

                        if economy_row == 0:
                            sys.stdout.write("\nAradığınız seferde ekonomi ya da business koltuğu bulunamadı!")
                            return ErrCodes.TEKRAR_DENE

                        print(f"Economy Row: {economy_row}, Business Row: {business_row}")

                        try:
                            economy_seat = WebDriverWait(self.driver, 10).until(
                                EC.visibility_of_element_located(
                                    (By.XPATH, f'/html/body/div/main/section/div[2]/div/div[1]/div/div/section/div[{row+1}]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[{economy_row}]/button/div/div[2]/div/div/span'))).text
                            business_seat = WebDriverWait(self.driver, 10).until(
                                EC.visibility_of_element_located(
                                    (By.XPATH, f'/html/body/div/main/section/div[2]/div/div[1]/div/div/section/div[{row+1}]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/button/div/div[2]/div/div/span'))).text
                        except TimeoutException:
                            sys.stdout.write("\nKoltuk bilgisi alınamadı, tekrar denenecek!")
                            return ErrCodes.TEKRAR_DENE

                        print(f"Economy Seat: {economy_seat}, Business Seat: {business_seat}")

                        try:
                            economy_seat = int(economy_seat[1:-1])
                            business_seat = int(business_seat[1:-1])
                        except ValueError:
                            sys.stdout.write("\nKoltuk bilgisi dönüştürülemedi, tekrar denenecek!")
                            return ErrCodes.TEKRAR_DENE

                        if economy_seat > 2 or business_seat > 2:
                            sys.stdout.write("\nTrende yeteri kadar boş yer mevcut!")
                            return ErrCodes.BASARILI
                        elif economy_seat in [1, 2]:
                            sys.stdout.write(f"\nEKONOMİ SINIFINDA Boş koltuk sayısı: {economy_seat} Acele et!!!!!")
                            return ErrCodes.BASARILI
                        elif business_seat in [1, 2]:
                            sys.stdout.write(f"\nBUSINESS SINIFINDA Boş koltuk sayısı: {business_seat} Acele et!!!!!")
                            return ErrCodes.BASARILI
                        else:
                            sys.stdout.write("\nAradığınız seferde şu an hiç boş yer yok ya da sadece engelli koltuğu mevcut!")
                            return ErrCodes.TEKRAR_DENE

                self.kill_driver()
                return ErrCodes.SAAT_HATASI
            else:
                sys.stdout.write("\nAradığınız seferde boş yer yoktur...")
                self.kill_driver()
                return ErrCodes.TEKRAR_DENE
        except TimeoutException:
            sys.stdout.write("\nZaman aşımına uğradı...")
            self.kill_driver()
            return ErrCodes.TIMEOUT_HATASI
        except NoSuchElementException:
            sys.stdout.write("\nAranan saat ya da sefer bulunamadı...")
            self.kill_driver()
            return ErrCodes.TEKRAR_DENE
        except UnexpectedAlertPresentException:
            sys.stdout.write("\nGüzergah bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz.")
            self.kill_driver()
            return ErrCodes.GUZERGAH_HATASI
        except Exception as e:
            sys.stdout.write(f"\nBilinmeyen bir hata oluştu: {e}")
            self.kill_driver()
            return ErrCodes.TEKRAR_DENE
