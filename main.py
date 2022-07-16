# -*- coding: utf-8 -*-
"""
@author: Birol Emekli
"""
from selenium import webdriver
from time import sleep
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import PySimpleGUI as sg
from threading import Thread

import Control, Rota, DriverSetting , DriverGet



class PushSafer():
    def sendNotification(self, baslik, mesaj):
        url = 'https://www.pushsafer.com/api'
        post_fields = {                      
            "t" : baslik,
            "m" : mesaj,
            "s" : 20,
            "pr": 2,
            "v" : 3,
            "i" : 9,
            "d" : 'a',
            "k" : "EbNquIM3VCj80rfoBL1K"
            }
        request = Request(url, urlencode(post_fields).encode())
        json = urlopen(request).read().decode()
        print(json)

pushSafer = PushSafer()

def driverSetting():
    return DriverSetting.DriverSetting().driverUP()

def driverGet(drivers):
    DriverGet.DriverGet(drivers).driverGet()

def rota(driver,first_location,last_location,date):
    Rota.Rota(driver, first_location, last_location, date).dataInput()

def control(driver,timee):
    response = Control.Control(driver,timee).sayfaKontrol()
    
    if response == "successful":
        
        pushSafer.sendNotification('TCDD Bilet Kontrol', "2'den fazla bilet bulundu")
        driver.quit()
        sys.exit()


font = ('Arial', 10)
sg.theme('DarkBlue')

layout = [  
            [[sg.Column([[sg.Text('TCDD')]], justification='center')]],
            [sg.Text('Nereden :',size=(7,1)), sg.Combo(['Gebze','Bilecik YHT'],default_value='Gebze',key='nereden')],
            [sg.Text('Nereye :',size=(7,1)), sg.Combo(['Gebze','Bilecik YHT'],default_value='Bilecik YHT',key='nereye')],
            [sg.Text('Tarih :',size=(7,1)), sg.InputText(['18.07.2022'],size=(14,5),key='tarih')],
            [sg.Text('Saat :',size=(7,1)), sg.InputText(['09:11'],size=(14,5),key='saat')],
            [sg.Button('Ara'), sg.Button('Durdur'),sg.Button('Kapat')]
         ]


window = sg.Window('Python App',layout,size = (250, 250),resizable = False,font=font)



def mainLoop():

    while True:
        
        driver = driverSetting()
        driverGet(driver)
        rota(driver,nereden,nereye,tarih)
        control(driver,saat)
        sleep(10)
    


while True:

    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == 'Kapat':
        
        window.close()
        sys.exit()

    if event == 'Ara':
        
        nereden = values['nereden']
        nereye  = values['nereye']
        tarih = '18.07.2022'
        saat = '09:11'
        
        th = Thread(target=mainLoop).start()

