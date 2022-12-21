# -*- coding: utf-8 -*-
"""
@author: Birol Emekli, https://github.com/bymcs, Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""
from selenium import webdriver
from time import sleep
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import PySimpleGUI as sg
from threading import Thread
from datetime import date
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
            "k" : "key"
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

font = ('Verdana', 10)
sg.theme('SystemDefault1')
today = date.today()
currentDate = today.strftime("%d.%m.%Y")

layout = [  
            [[sg.Column([[sg.Text('TCDD Bilet Arama Botu')]], justification='center')]],
            [sg.Text('Nereden :',size=(7,1)), sg.Combo(['İstanbul(Söğütlü Ç.)', 'İstanbul(Pendik)', 'Gebze','Bilecik YHT','Eskişehir', 'Ankara Gar'],default_value='İstanbul(Söğütlü Ç.)',key='nereden')],
            [sg.Text('Nereye :',size=(7,1)), sg.Combo(['İstanbul(Söğütlü Ç.)', 'İstanbul(Pendik)', 'Gebze','Bilecik YHT','Eskişehir', 'Ankara Gar'],default_value='Ankara Gar',key='nereye')],
            [sg.Text('Tarih :',size=(7,1)), sg.InputText(currentDate,size=(14,5),key='tarih')],
            [sg.Text('Saat :',size=(7,1)), sg.InputText(['09:11'],size=(14,5),key='saat')],
            [sg.Button('Aramaya Başla'), sg.Button('Durdur!'),sg.Button('Kapat!')],
            [sg.Text('Mesaj :',size=(6,1)), sg.Multiline("",size=(22,8),key='log',autoscroll=True, reroute_stdout=True,)]
         ]

window = sg.Window('TCDD Bilet Arama Botu',layout,size = (300, 250),resizable = False,font=font, element_justification='l')


def mainLoop():

    while True:   
        driver = driverSetting()
        driverGet(driver)
        rota(driver,nereden,nereye,tarih)
        control(driver,saat)
        sleep(30)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Kapat':
        window.close()
        sys.exit()

    if event == 'Aramaya Başla':
        nereden = values['nereden']
        nereye  = values['nereye']
        tarih = values['tarih']
        saat = values['saat']
        th = Thread(target=mainLoop).start()
            

