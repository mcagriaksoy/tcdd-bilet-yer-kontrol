# -*- coding: utf-8 -*-
"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced version @author: Mehmet Çağrı Aksoy https://github.com/mcagriaksoy
"""

from os import path, system
import platform
from datetime import date, datetime
from time import sleep
from threading import Thread

if platform.system() == "Windows":
    import winsound

import Control
import DriverGet
import DriverSetting
import Sehirler
import Rota

import error_codes as ErrCodes
import PySimpleGUI as sg


def main():
    def driver_setting():
        """Driver'ı ayarlar."""
        return DriverSetting.DriverSetting().driver_init()

    def driver_get(drivers):
        """Driver'ı alır ve sayfayı yükler."""
        DriverGet.DriverGet(drivers).driver_get()

    def route(driver, first_location, last_location, date):
        """ Rota bilgilerini alır ve gerekli yerlere yazar.""" ""
        isError = Rota.Rota(driver, first_location, last_location, date).dataInput()
        if isError == -1:
            window["Aramaya Başla"].update(disabled=False)
            window["Durdur!"].update(disabled=True)
            driver.quit()
            exit()

    def kill_chrome():
        """Chrome'u kapatır."""
        if platform == "win32":
            system("taskkill /im chrome.exe /f")
        else:
            system("pkill chrome")

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
            """
            # Telegram mesaji gonder!
            if telegram_msg:
                TelegramMsg.TelegramMsg().send_telegram_message(bot_token, chat_id)
            """
            sg.Popup(
                "Hey Orada mısın? Biletin bulundu. Satın alabilirsin ❤️❤️❤️❤️",
                keep_on_top=True,
                button_type=5,
            )

        elif response == ErrCodes.TEKRAR_DENE:
            print("\n" + str(delay_time) + " Dakika icerisinde tekrar denenecek...")

        else:
            window["Aramaya Başla"].update(disabled=False)
            window["Durdur!"].update(disabled=True)

        # Chrome'u kapat!
        # kill_chrome()

    # GUI Ayarlari
    font = ("Verdana", 10)
    sg.theme("SystemDefault1")
    today = date.today()
    currentDate = today.strftime("%d.%m.%Y")

    now = datetime.now()
    currentTime = now.strftime("%H:%M")

    sg.popup(
        "💖 Selam, Hos geldin 💖",
        "Ilk defa kullaniyorsaniz, ilk taramada biraz bekleyebilirsiniz!",
        keep_on_top=True,
    )
    layout = [
        [
            [
                sg.Column(
                    [[sg.Text("by Mehmet Cagri Aksoy 2022-2024")]],
                    justification="center",
                )
            ]
        ],
        [
            sg.Text("Nereden :", size=(7, 1)),
            sg.Combo(
                Sehirler.sehir_listesi,
                default_value="İstanbul(Söğütlüçeşme)",
                key="nereden",
            ),
        ],
        [
            sg.Text("Nereye :", size=(7, 1)),
            sg.Combo(Sehirler.sehir_listesi, default_value="Ankara Gar", key="nereye"),
        ],
        [
            sg.CalendarButton(
                "Takvim",
                target="tarih",
                format="%d.%m.%Y",
                default_date_m_d_y=(3, 26, 2024),
            ),
            sg.Input(key="tarih", size=(20, 1), default_text=currentDate),
        ],
        [
            sg.Text("Saat :", size=(7, 1)),
            sg.InputText(default_text=currentTime, size=(14, 5), key="saat"),
        ],
        [sg.Text("Arama Sıklığını seçiniz: (dakikada bir)")],
        [
            sg.Slider(
                range=(1, 10),
                key="delay_time",
                orientation="h",
                size=(35, 25),
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
        [sg.Button("Aramaya Başla"), sg.Button("Durdur!"), sg.Button("Kapat!")],
        [
            sg.Multiline(
                "", size=(32, 8), key="log", autoscroll=True, reroute_stdout=True
            )
        ],
    ]

    window = sg.Window(
        "TCDD Bilet Arama Botu",
        layout,
        icon=r"./icon.ico",
        size=(320, 565),
        resizable=False,
        font=font,
        element_justification="l",
    ).Finalize()
    window["Durdur!"].update(disabled=True)

    def thread1(delay_time, telegram_msg, bot_token, chat_id, ses):
        """Arama dongusu!"""
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
        # Control.Control(data, None).kill_driver()
        kill_chrome()
        print("Web Surucusu Kapandi!")

    while True:
        event, values = window.read()
        # driver = None

        if event == sg.WIN_CLOSED or event == "Kapat!":
            window.close()
            break

        if event == "Durdur!":
            window["Aramaya Başla"].update(disabled=False)
            window["Durdur!"].update(disabled=True)
            t2 = Thread(target=thread2)
            t2.start()

        if event == "Aramaya Başla":
            nereden = values["nereden"]
            nereye = values["nereye"]
            tarih = values["tarih"]
            saat = values["saat"]
            
            if saat == "":
                sg.popup("Lütfen saat bilgisini giriniz!")
                continue
            elif tarih == "":
                sg.popup("Lütfen tarih bilgisini giriniz!")
                continue
            elif nereden == nereye:
                sg.popup("Nereden ve Nereye aynı olamaz!")
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
            bot_token = values["bot_token"]
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
