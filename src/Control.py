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
                                        UnexpectedAlertPresentException)
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
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "mainTabView:gidisSeferTablosu")))
            if element:
                sys.stdout.write("\nAranan  saat : " + self.zaman + "\n")
                for row in range(1, MAX_TREN_SAYISI):
                    sleep(0.2)
                    xpath = f'//*[@id="mainTabView:gidisSeferTablosu_data"]/tr[{row}]/td[1]/span'
                    aranan_element = WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(
                        (By.XPATH, xpath)))
                    aranan = aranan_element.text
                    sleep(0.2)
                    if self.zaman == aranan:
                        sys.stdout.write("\nAranan saat bulundu...")
                        message_element = WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(
                            (By.XPATH, f'//*[@id="mainTabView:gidisSeferTablosu:{row-1}:j_idt109:0:somVagonTipiGidis1_label"]'.format(row))))
                        message = message_element.text
                        
                        # Search pattern of ) (
                        match = search(r'\) \(.', message)
                        if match is None:
                            sys.stdout.write(
                                "\nSayfa yüklenirken hata oluştu...")
                            return ErrCodes.TEKRAR_DENE
                        koltuk_sayisi = int(match.group()[3])
                        if koltuk_sayisi > 2:
                            sys.stdout.write(
                                f"\nTrende yeteri kadar bos ver mevcut!")
                            return ErrCodes.BASARILI
                        elif koltuk_sayisi == 2 or koltuk_sayisi == 1:
                            sys.stdout.write(
                                f"\nBoş koltuk sayısı: {koltuk_sayisi} Sadece Engelli Bileti Kaldı!")
                            return ErrCodes.TEKRAR_DENE
                        elif koltuk_sayisi == 0:
                            sys.stdout.write(
                                "\nAradığınız seferde hiç boş yer yok...")
                            return ErrCodes.TEKRAR_DENE
                    #else:
                        #sys.stdout.write("\nSaatler inceleniyor Adim: " + str(row))
                self.kill_driver()
                return ErrCodes.SAAT_HATASI
                    
            else:
                sys.stdout.write("\nAradığınız seferde boş yer yoktur...")
                message = ""
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
        except UnexpectedAlertPresentException as ex1:
            sys.stdout.write(
                f"\nGüzergah bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz. İstasyonları doğru girdiğinizden emin olunuz.\n")
            self.kill_driver()
            return ErrCodes.GUZERGAH_HATASI
