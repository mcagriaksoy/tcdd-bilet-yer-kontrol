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

def driverSetting():
    return DriverSetting.DriverSetting().driverUP()

def driverGet(drivers):
    DriverGet.DriverGet(drivers).driverGet()

def rota(driver,first_location,last_location,date):
    Rota.Rota(driver, first_location, last_location, date).dataInput()

def control(driver,timee):
    response = Control.Control(driver,timee).sayfaKontrol()
    if response == "successful":
        clicked = sg.Popup('Hey Orada mısın? Biletin bulundu. Satın alabilirsin', keep_on_top=True,  button_type=5)
        if clicked == 'OK':
            sys.stdout.write('\nPopup Kapatildi!')
        driver.quit()
        sys.exit()

font = ('Verdana', 10)
sg.theme('SystemDefault1')
today = date.today()
currentDate = today.strftime("%d.%m.%Y")

layout = [  
            [[sg.Column([[sg.Text('github.com/mcagriaksoy')]], justification='center')]],
            [sg.Text('Nereden :',size=(7,1)), sg.Combo(['İstanbul(Söğütlü Ç.)','İstanbul(Bakırköy)', 'İstanbul(Halkalı)', 'İstanbul(Pendik)', 'Gebze','Bilecik YHT','Eskişehir', 'Ankara Gar', 'Konya'],default_value='İstanbul(Söğütlü Ç.)',key='nereden')],
            [sg.Text('Nereye :',size=(7,1)), sg.Combo(['İstanbul(Söğütlü Ç.)', 'İstanbul(Bakırköy)', 'İstanbul(Halkalı)', 'İstanbul(Pendik)', 'Gebze','Bilecik YHT','Eskişehir', 'Ankara Gar', 'Konya'],default_value='Ankara Gar',key='nereye')],
            [sg.Text('Tarih :',size=(7,1)), sg.InputText(currentDate,size=(14,5),key='tarih')],
            [sg.Text('Saat :',size=(7,1)), sg.InputText(['09:11'],size=(14,5),key='saat')],
            [sg.Text('Arama Sıklığını seçiniz: (dakikada bir)')],
            [sg.Slider(range=(1, 10), key='delayTime', orientation='h', size=(35, 25), default_value=1, enable_events=True)],
            [sg.Button('Aramaya Başla'), sg.Button('Durdur!'),sg.Button('Kapat!')],
            [sg.Multiline("",size=(32,8),key='log',autoscroll=True, reroute_stdout=True)]
         ]

window = sg.Window('TCDD Bilet Arama Botu',layout, icon=r'icon.ico', size = (300, 350),resizable = False,font=font, element_justification='l')

def mainLoop():

    while True:   
        driver = driverSetting()
        driverGet(driver)
        rota(driver,nereden,nereye,tarih)
        control(driver,saat)
        sleep(delayTime)

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
        delayTime = values['delayTime']
        th = Thread(target=mainLoop).start()
            

