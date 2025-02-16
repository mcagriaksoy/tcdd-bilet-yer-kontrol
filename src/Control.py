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
                EC.visibility_of_element_located((By.XPATH, '//*[@id="seferListScroll"]/div[2]/div/div[1]')))
            if element:
                sys.stdout.write("\nAranan  saat : " + self.zaman + "\n")
                for row in range(0, MAX_TREN_SAYISI):
                    sleep(0.2)
                    xpath = f'//*[@id="gidis{row}btn"]/div/div[2]/div/div[2]/div[2]/span[1]/time'
                    aranan_element = WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(
                        (By.XPATH, xpath)))
                    aranan = aranan_element.text
                    sleep(0.2)
                    if self.zaman == aranan:
                        sys.stdout.write("\nAranan saat bulundu...")
                        # click xpath above
                        element = WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable(
                            (By.XPATH, xpath)))
                        element.click()
                        #koltuk_xpath "/html/body/div/main/section/div[2]/div/div[1]/div/div/section/div[8]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/button/div/div[2]/div/div/span/text()"
                        message_element = WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(
                            (By.XPATH, f'/html/body/div/main/section/div[2]/div/div[1]/div/div/section/div[{row+1}]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/button/div/div[2]/div/div/span')))
                        economy_seat = message_element.text

                        message_element = WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(
                            (By.XPATH, f'/html/body/div/main/section/div[2]/div/div[1]/div/div/section/div[{row+1}]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/button/div/div[2]/div/div/span')))
                        business_seat = message_element.text
                        
                        # delete first and last characters
                        economy_seat = economy_seat[1:-1]
                        business_seat = business_seat[1:-1]

                        sys.stdout.write(economy_seat)
                        sys.stdout.write(business_seat)

                        # convert to integer
                        economy_seat = int(economy_seat)
                        business_seat = int(business_seat)

                        if economy_seat > 2 or business_seat > 2:
                            sys.stdout.write(
                                "\nTrende yeteri kadar bos ver mevcut!")
                            return ErrCodes.BASARILI
                        elif economy_seat == 2 or economy_seat == 1:
                            sys.stdout.write(
                                f"\nEKONOMI SINIFINDA Boş koltuk sayısı: {economy_seat} Acele et!!!!!")
                            return ErrCodes.BASARILI
                        elif business_seat == 2 or business_seat == 1:
                            sys.stdout.write(
                                f"\nBUSINESS SINIFINDA Boş koltuk sayısı: {business_seat} Acele et!!!!!")
                            return ErrCodes.BASARILI
                        else:
                            sys.stdout.write(
                                "\nAradığınız seferde suan hiç boş yer yok...")
                            return ErrCodes.TEKRAR_DENE
                    #else:
                        #sys.stdout.write("\nSaatler inceleniyor Adim: " + str(row))
                self.kill_driver()
                return ErrCodes.SAAT_HATASI
                    
            else:
                sys.stdout.write("\nAradığınız seferde boş yer yoktur...")
                economy_seat = ""
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
