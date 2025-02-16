# -*- coding: utf-8 -*-
"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced (Forked) version @author: Mehmet C. Aksoy https://github.com/mcagriaksoy
"""

import os
import platform
from datetime import date, datetime
from time import sleep
from threading import Thread

import error_codes as ErrCodes
import PySimpleGUI as sg
from webbrowser import open as wbopen
if platform.system() == "Windows":
    import winsound

import Control
import DriverGet
import DriverSetting
import Sehirler
import Rota
import TelegramMsg

g_isStopped = False

FULL_SIZE = (310, 777)
HALF_SIZE = (310, 647)

def main():
    def driver_setting():
        """Driver'ı ayarlar."""
        return DriverSetting.DriverSetting().driver_init()

    def driver_get(drivers):
        """Driver'ı alır ve sayfayı yükler."""
        DriverGet.DriverGet(drivers).driver_get()

    def route(driver, first_location, last_location, date):
        """ Rota bilgilerini alır ve gerekli yerlere yazar."""
        global g_isStopped
        isError = Rota.Rota(driver, first_location, last_location, date).dataInput()
        if isError == -1 or g_isStopped == True:
            window["Aramaya Başla"].update(disabled=False)
            window["Durdur!"].update(disabled=True)
            driver.quit()
            return

    def control(driver, time, delay_time, telegram_msg, bot_token, chat_id, ses):
        """Sayfada yer var mı yok mu kontrol eder."""
        response = Control.Control(driver, time).sayfa_kontrol()
        if response == ErrCodes.BASARILI:
            # Ses cal!
            if ses:
                for i in range(5):
                    if platform.system() == "Windows":
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                    elif platform.system() == "Darwin" or platform.system() == "Linux":
                        os.system('play -n synth 0.1 sine 660')

            # Telegram mesaji gonder!
            if telegram_msg:
                TelegramMsg.TelegramMsg().send_telegram_message(bot_token, chat_id)

            # Make popup always on top
            sg.Popup(
                "Hey Orada mısın? Biletin bulundu. Satın alabilirsin ❤️❤️❤️❤️",
                keep_on_top=True,
                button_type=5,
            )

        elif response == ErrCodes.TEKRAR_DENE:
            print("\n" + str(delay_time) + " Dakika icerisinde tekrar denenecek...")
            # Close the driver
            driver.quit()
        
        elif response == ErrCodes.TIMEOUT_HATASI:
            delay_time = 0
            # Close the driver
            driver.quit()

        else:
            window["Aramaya Başla"].update(disabled=False)
            window["Durdur!"].update(disabled=True)

    # GUI Ayarlari
    font = ("Verdana", 10)
    sg.theme("SystemDefault1")
    today = date.today()
    currentDate = today.strftime("%d.%m.%Y")
    # extract day, month, year
    day = currentDate.split(".")[0]
    month = currentDate.split(".")[1]
    year = currentDate.split(".")[2]

    now = datetime.now()
    currentTime = now.strftime("%H:%M")

    sg.popup(
        "Merhaba, Hos geldin :)",
        "Ilk defa kullaniyorsaniz, ilk taramada biraz bekleyebilirsiniz!",
        keep_on_top=True,
        auto_close=True,
        auto_close_duration=10,
        title = "",
        non_blocking=True
    
    )

    layout = [
        [
            [
                sg.Column(
                    [[sg.Text("by Mehmet C. Aksoy 2022-2025")]],
                    justification="center",
                )
            ]
        ],
        [
            sg.Column(
                [[sg.Button('', image_filename='donate.jpg', key='donate', button_color=('black', 'black'), size=(10, 1))]],
                justification="center",
                element_justification="center",
                expand_x=True,
            )
        ],
            
        [sg.Button("TCDD Sitesine git!", size=(20, 1)),
         sg.Button("Yardım", size=(20, 1)),
        ],
        [
            sg.Text("Nereden :", size=(7, 1)),
            sg.Combo(
                Sehirler.sehir_listesi,
                default_value="Eskişehir",
                key="nereden",
                enable_events=True,
                #readonly=True
            ),
        ],
        [
            sg.Text("Nereye :", size=(7, 1)),
            sg.Combo(
             Sehirler.sehir_listesi,
             default_value="Ankara Gar",
             key="nereye",
             enable_events=True,
            ),
        ],
        [
            sg.Text("Arama yapılacak bilet türünü seçiniz:"),
        ],
        [
            sg.Checkbox("Ekonomi", default=True, key="ekonomi"),
            sg.Checkbox("Business", default=True, key="business"),
        ],
        [
            sg.CalendarButton(
                "Takvim ",
                target="tarih",
                format="%d.%m.%Y",
                default_date_m_d_y=(int(month), int(day), int(year)),
            ),
            sg.Input(key="tarih", size=(14, 1), default_text=currentDate),
            sg.Button("Bugün", size=(6, 1)),
        ],
        [
            sg.Text("Saat:", size=(7, 1)),
            sg.InputText(default_text=currentTime, size=(14, 5), key="saat"),
        ],

        [sg.Text("Arama Sıklığını seçiniz: (dakikada bir)")],
        [
            sg.Slider(
                range=(1, 30),
                key="delay_time",
                orientation="h",
                size=(35, 20),
                default_value=1,
                enable_events=True,
            )
        ],
        [sg.Text("Telegram Ayarlari: (Opsiyonel)")],
        [
            sg.Checkbox(
                "Bilet bulunursa telegram mesaji gönder!",
                default=False,
                key="telegram_msg",
            )
        ],
        [sg.Text("Telegram Bot Token:")],
        [sg.InputText(key="bot_token", size=(35, 5))],
        [sg.Text("Telegram Chat ID:")],
        [sg.InputText(key="chat_id", size=(35, 5))],
        [sg.Text("Ses Ayarlari: (Opsiyonel)")],
        [sg.Checkbox("Bilet bulunursa ses çal!", default=True, key="ses")],
        [sg.Button("Aramaya Başla"), sg.Button("Durdur!"), sg.Button("Kapat!"), sg.Button("↑")],
        [
            sg.Multiline(
                "", size=(32, 8), key="log", autoscroll=True, reroute_stdout=True
            )
        ],
    ]

    window = sg.Window(
        "TCDD Otomatik Bilet Arama Programı",
        layout,
        icon=r"./icon.ico",
        size=FULL_SIZE,
        resizable=False,
        font=font,
        element_justification="l",
    ).Finalize()

    window["Durdur!"].update(disabled=True)
    window['nereden'].bind('<KeyRelease>', 'KEY')
    window['nereye'].bind('<KeyRelease>', 'KEY')

    def thread1(delay_time, telegram_msg, bot_token, chat_id, ses):
        """Arama dongusu!"""
        global g_isStopped
        g_isStopped = False

        while True:
            """ Arama dongusu!"""
            driver = driver_setting()
            driver_get(driver)
            route(driver, nereden, nereye, tarih)
            control(driver, saat, delay_time, telegram_msg, bot_token, chat_id, ses)
            sleep(30)

    def thread2():
        """Durdurma dongusu!"""
        window["log"].update(value="")

    while True:
        event, values = window.read()

        if event == "donate":
            wbopen("https://www.buymeacoffee.com/mcagriaksoy")

        if event == "Bugün":
            window["tarih"].update(currentDate)

        if event == "↑":
            if window.size == FULL_SIZE:
                window["↑"].update("↓")
                window.size = HALF_SIZE
            else:
                window["↑"].update("↑")
                window.size = FULL_SIZE

        if event == sg.WIN_CLOSED or event == "Kapat!":
            window.close()
            break

        if event == "Durdur!":
            window["Aramaya Başla"].update(disabled=False)
            window["Durdur!"].update(disabled=True)
            global g_isStopped
            g_isStopped = True
            t2 = Thread(target=thread2)
            t2.start()

        if event == "Yardım":
            #print url

            if(sg.popup_yes_no("Yardım sayfasına gitmek ister misiniz?", keep_on_top=True)) == "Yes":
                wbopen("https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol")

        
        if event == "TCDD Sitesine git!":
            sg.popup_no_buttons("TCDD Bilet Satış Sitesine yönlendiriliyorsunuz. Lütfen bekleyin...",
             auto_close=True, auto_close_duration=1, no_titlebar=True)
            wbopen("https://ebilet.tcddtasimacilik.gov.tr")
        
        if event == "neredenKEY":
            #Get pressed Key from keyboard
            current_input = values["nereden"]
            # Filter the items based on the current input
            filtered_items = [item for item in Sehirler.sehir_listesi if item.lower().startswith(current_input.lower())]
            # Update the combo box with the filtered items
            window["nereden"].update(values=filtered_items, value=current_input)
        elif event == "nereyeKEY":
            #Get pressed Key from keyboard
            current_input = values["nereye"]
            # Filter the items based on the current input
            filtered_items = [item for item in Sehirler.sehir_listesi if item.lower().startswith(current_input.lower())]
            # Update the combo box with the filtered items
            window["nereye"].update(values=filtered_items, value=current_input)

        if event == "Aramaya Başla":
            nereden = values["nereden"]
            nereye = values["nereye"]
            tarih = values["tarih"]
            saat = values["saat"]
            business = values["business"]
            ekonomi = values["ekonomi"]
            
            if saat == "":
                sg.popup("Lütfen saat bilgisini giriniz!")
                continue
            elif tarih == "":
                sg.popup("Lütfen tarih bilgisini giriniz!")
                continue
            elif nereden == nereye:
                sg.popup("Nereden ve Nereye aynı olamaz!")
                continue
            elif business == False and ekonomi == False:
                sg.popup("Lütfen bilet türünü seçiniz!")
                continue

            if "/" in tarih:
                tarih = tarih.replace("/", ".")
            elif "-" in tarih:
                tarih = tarih.replace("-", ".")

            # If saat has , . replace with :
            if "." in saat:
                saat = saat.replace(".", ":")
            elif "," in saat:
                saat = saat.replace(",", ":")

            delay_time = values["delay_time"]

            telegram_msg = values["telegram_msg"]
            if telegram_msg:
                if values["bot_token"] == "" or values["chat_id"] == "":
                    sg.popup("Telegram bot token ve chat id bilgilerini giriniz!")
                    continue

            bot_token = values["bot_token"]
            if (bot_token != "") and not TelegramMsg.TelegramMsg().check_telegram_bot_status(bot_token):
                sg.popup("Telegram bot token bilgisi hatali! kontrol ediniz!")
                continue

            chat_id = values["chat_id"]        
            ses = values["ses"]

            window["Aramaya Başla"].update(disabled=True)
            window["Durdur!"].update(disabled=False)

            print("Arama başladı. Lütfen bekleyin...")
            t1 = Thread(
                target=thread1, args=(delay_time, telegram_msg, bot_token, chat_id, ses)
            )
            t1.start()

def __main__():
    main()
