# -*- coding: utf-8 -*-
"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""
import sys
from time import sleep

import error_codes as ErrCodes
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Control:
    ''' Class: Sayfada yer var mı yok mu kontrol eder.'''

    def __init__(self, driver, time):
        ''' Constructor methodu.'''
        self.driver = driver
        self.zaman = time

    def kill_driver(self):
        ''' Driver'ı kapatır.'''
        self.driver.close()
        self.driver.quit()

    def sayfa_kontrol(self):
        ''' Sayfada yer var mı yok mu kontrol eder.'''
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "mainTabView:gidisSeferTablosu_data")))
            if element != "":
                sys.stdout.write("\nAranan  saat : " + self.zaman + "\n")
                for row in range(1, 15):
                    try:
                        sys.stdout.write(".")
                        aranan_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                            (By.XPATH, f'/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/table/tbody/tr[{0}]/td[1]/span'.format(row))))
                        aranan = aranan_element.text
                        sleep(0.3)
                        if self.zaman == aranan:
                            sleep(0.3)
                            message_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                                (By.XPATH, f'//*[@id="mainTabView:gidisSeferTablosu:{0}:j_idt109:0:somVagonTipiGidis1_label"]'.format(row - 1))))
                            message = message_element.text
                            if message[22] != '0':

                                if int(message[22]) > 2:
                                    sys.stdout.write(
                                        "\nBoş koltuk sayısı: " + message[22] + message[23])
                                    sys.stdout.write(
                                        "\nHARİKA! Fazla bilet bulundu.. Satın Alabilirsin")
                                    return ErrCodes.BASARILI
                                else:
                                    sys.stdout.write(
                                        "\nBoş koltuk sayısı: " + message[22] + " Sadece Engelli Bileti Kaldı!")
                                    return ErrCodes.TEKRAR_DENE

                            else:
                                sys.stdout.write(
                                    "\nAradığınız seferde hiç boş yer yok...")
                                return ErrCodes.TEKRAR_DENE

                    except NoSuchElementException:
                        sys.stdout.write("\nSaatinizde hata var...")
                        self.kill_driver()
                        return ErrCodes.SAAT_HATASI
            else:
                sys.stdout.write("\nAradığınız seferde boş yer yoktur...")
                message = ""
                self.kill_driver()
                return ErrCodes.TEKRAR_DENE

        except (TimeoutException, NoSuchElementException):
            message = ""
            self.kill_driver()
            return ErrCodes.TEKRAR_DENE

        except UnexpectedAlertPresentException as ex1:
            sys.stdout.write(
                f"\nGüzergah bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz. İstasyonları doğru girdiğinizden emin olunuz.\nHata Kodu: {ex1.msg}")
            self.kill_driver()
            return ErrCodes.GUZERGAH_HATASI
