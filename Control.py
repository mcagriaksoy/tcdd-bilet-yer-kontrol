# -*- coding: utf-8 -*-
"""
@author: Birol Emekli, Mehmet Çağrı Aksoy
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException,UnexpectedAlertPresentException
from time import sleep
import sys

class Control:
    def __init__(self,driver,time):
        self.driver=driver
        self.zaman=time

    def sayfaKontrol(self):  

        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "mainTabView:gidisSeferTablosu_data")))
            if element != "":
                sys.stdout.write("\nAranan  saat : " + self.zaman)
                for row in range(1, 15):
                    try:
                         aranan = self.driver.find_element(By.XPATH ,'/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/table/tbody/tr[{0}]/td[1]/span'.format(row)).text 
                         sleep(0.3)
                         if self.zaman == aranan:
                            sleep(0.5)
                            message=self.driver.find_element(By.XPATH ,'//*[@id="mainTabView:gidisSeferTablosu:{0}:j_idt109:0:somVagonTipiGidis1_label"]'.format(row - 1)).text
                            if message[22] != '0':
                                
                                if int(message[22]) > 2:
                                    sys.stdout.write("\nBoş koltuk sayısı: "+ message[22] + message[23])
                                    sys.stdout.write("\nHARİKA! Fazla bilet bulundu.. Satın Alabilirsin")
                                    return "successful"
                                else:
                                    sys.stdout.write("\nBoş koltuk sayısı: "+ message[22] +" Sadece Engelli Bileti Kaldı!")
                                    sys.stdout.write("\nArama tekrar deneniyor...")
                                    message = ""
                                    self.driver.quit()
                                    return
                                
                            else:
                                sys.stdout.write("\nAradığınız seferde hiç boş yer yok...")
                                self.driver.quit()
                                message = ""
                                return
                    except:
                        sys.stdout.write("\nSaatinizde hata var...")
                        return
                        #self.driver.quit()
                        #sys.exit()
            else:
                sys.stdout.write("\nAradığınız seferde boş yer yoktur...")

        except (TimeoutException,NoSuchElementException) as ex:
            sys.stdout.write("\nTekrar deneniyor...")
            self.driver.close()
            return
        except UnexpectedAlertPresentException as ex1:
            sys.stdout.write("\nGüzergah bilgilerinde hata meydana geldi. Kontrol ederek tekrar deneyiniz. İstasyonları doğru girdiğinizden emin olunuz")
            self.driver.quit()
            exit()       
