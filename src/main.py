# -*- coding: utf-8 -*-
"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""

import datetime
import sys
from datetime import date
from pydoc import cli
from threading import Thread
from time import sleep
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import Control
import DriverGet
import DriverSetting
import error_codes as ErrCodes
import PySimpleGUI as sg
import Rota
from selenium import webdriver

if sys.platform == "win32":
    import winsound
else:
    import os


def driver_setting():
    ''' Driver'ı ayarlar.'''
    return DriverSetting.DriverSetting().driver_init()


def driver_get(drivers):
    ''' Driver'ı alır ve sayfayı yükler.'''
    DriverGet.DriverGet(drivers).driver_get()


def route(driver, first_location, last_location, date):
    ''' Rota bilgilerini alır ve gerekli yerlere yazar.'''''
    isError = Rota.Rota(driver, first_location,
                        last_location, date).dataInput()
    if isError == -1:
        window['Aramaya Başla'].update(disabled=False)
        window['Durdur!'].update(disabled=True)
        driver.quit()
        exit()


def kill_chrome():
    ''' Chrome'u kapatır. '''
    if sys.platform == "win32":
        os.system("taskkill /im chrome.exe /f")
    else:
        os.system("pkill chrome")


def control(driver, time, delayTime):
    ''' Sayfada yer var mı yok mu kontrol eder.'''
    response = Control.Control(driver, time).sayfa_kontrol()
    if response == ErrCodes.BASARILI:
        sg.Popup('Hey Orada mısın? Biletin bulundu. Satın alabilirsin',
                 keep_on_top=True,
                 button_type=5)

        if sys.platform == "win32":
            winsound.Beep(440, 20000)
        else:
            os.system("beep -f 440 -l 20000")
        kill_chrome()
        return

    elif response == ErrCodes.TEKRAR_DENE:
        print("\n" + str(delayTime) + " Dakika icerisinde tekrar denenecek...")

    else:
        window['Aramaya Başla'].update(disabled=False)
        window['Durdur!'].update(disabled=True)
        kill_chrome()
        return


# GUI Ayarlari
font = ('Verdana', 10)
sg.theme('SystemDefault1')
today = date.today()
currentDate = today.strftime("%d.%m.%Y")

now = datetime.datetime.now()
currentTime = now.strftime("%H:%M")

layout = [
    [[sg.Column([[sg.Text('github.com/mcagriaksoy')]], justification='center')]],
    [sg.Text('Nereden :', size=(7, 1)), sg.Combo(['İstanbul(Söğütlüçeşme)', 'İstanbul(Bakırköy)', 'İstanbul(Halkalı)', 'İstanbul(Pendik)',
                                                  'Gebze', 'Bilecik YHT', 'Eskişehir', 'Ankara Gar', 'Konya', 'Kars', 'Erzurum'], default_value='İstanbul(Söğütlüçeşme)', key='nereden')],
    [sg.Text('Nereye :', size=(7, 1)), sg.Combo(['İstanbul(Söğütlüçeşme)', 'İstanbul(Bakırköy)', 'İstanbul(Halkalı)', 'İstanbul(Pendik)',
                                                 'Gebze', 'Bilecik YHT', 'Eskişehir', 'Ankara Gar', 'Konya', 'Kars', 'Erzurum'], default_value='Ankara Gar', key='nereye')],
    [sg.CalendarButton('Takvim',  target='tarih', format='%d.%m.%Y', default_date_m_d_y=(
        12, 12, 2023)), sg.Input(key='tarih', size=(20, 1), default_text=currentDate)],
    [sg.Text('Saat :', size=(7, 1)), sg.InputText(
        default_text=currentTime, size=(14, 5), key='saat')],
    [sg.Text('Arama Sıklığını seçiniz: (dakikada bir)')],
    [sg.Slider(range=(1, 10), key='delayTime', orientation='h', size=(
        35, 25), default_value=1, enable_events=True)],
    [sg.Button('Aramaya Başla'), sg.Button('Durdur!'), sg.Button('Kapat!')],
    [sg.Multiline("", size=(32, 8), key='log',
                  autoscroll=True, reroute_stdout=True)]
]

window = sg.Window('TCDD Bilet Arama Botu',
                   layout,
                   icon=r'./icon.ico',
                   size=(300, 350),
                   resizable=False,
                   font=font,
                   element_justification='l').Finalize()
window['Durdur!'].update(disabled=True)


def thread1(delayTime):
    while True:
        ''' Arama dongusu!'''
        driver = driver_setting()
        driver_get(driver)
        route(driver, nereden, nereye, tarih)
        control(driver, saat, delayTime)
        sleep(30)


def thread2():
    ''' Durdurma dongusu! '''
    window['log'].update(value='')
    # Control.Control(data, None).kill_driver()
    kill_chrome()
    print('Web Surucusu Kapandi!')


while True:
    event, values = window.read()
    # driver = None

    if event == sg.WIN_CLOSED or event == 'Kapat!':
        window.close()
        break

    if event == 'Durdur!':
        window['Aramaya Başla'].update(disabled=False)
        window['Durdur!'].update(disabled=True)
        t2 = Thread(target=thread2)
        t2.start()

    if event == 'Aramaya Başla':
        window['Aramaya Başla'].update(disabled=True)
        window['Durdur!'].update(disabled=False)
        nereden = values['nereden']
        nereye = values['nereye']
        tarih = values['tarih']
        saat = values['saat']
        delayTime = values['delayTime']
        t1 = Thread(target=thread1, args=(delayTime,))
        t1.start()
