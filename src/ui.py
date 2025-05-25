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
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkinter.scrolledtext import ScrolledText
from tkcalendar import DateEntry

import error_codes as ErrCodes
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
        # ...existing code...
        return DriverSetting.DriverSetting().driver_init()

    def driver_get(drivers):
        # ...existing code...
        DriverGet.DriverGet(drivers).driver_get()

    def route(driver, first_location, last_location, date_):
        # ...existing code...
        global g_isStopped
        isError = Rota.Rota(driver, first_location, last_location, date_).dataInput()
        if isError == -1 or g_isStopped == True:
            btn_start.config(state=tk.NORMAL)
            btn_stop.config(state=tk.DISABLED)
            driver.quit()
            return

    def control(driver, time, delay_time, telegram_msg, bot_token, chat_id, ses):
        # ...existing code...
        response = Control.Control(driver, time).sayfa_kontrol()
        if response == ErrCodes.BASARILI:
            if ses:
                try:
                    for _ in range(5):  # Play the sound 5 times
                        winsound.Beep(1000, 500)  # Frequency: 1000 Hz, Duration: 500 ms
                        sleep(0.1)  # Short delay between beeps
                except Exception as e:
                    print(f"Failed to play sound: {e}")
            if telegram_msg:
                TelegramMsg.TelegramMsg().send_telegram_message(bot_token, chat_id)
            messagebox.showinfo("Bilet Bulundu", "Hey Orada mısın? Biletin bulundu. Satın alabilirsin ❤️❤️❤️❤️")
        elif response == ErrCodes.TEKRAR_DENE:
            log_text.insert(tk.END, f"\n{delay_time} Dakika icerisinde tekrar denenecek...")
            driver.quit()
        elif response == ErrCodes.TIMEOUT_HATASI:
            delay_time = 0
            driver.quit()
        else:
            btn_start.config(state=tk.NORMAL)
            btn_stop.config(state=tk.DISABLED)

    # GUI Ayarlari
    today = date.today()
    currentDate = today.strftime("%d.%m.%Y")
    day, month, year = currentDate.split(".")
    now = datetime.now()
    currentTime = now.strftime("%H:%M")

    root = tk.Tk()
    root.title("TCDD Otomatik Bilet Arama Programı")
    root.geometry(f"{HALF_SIZE[0]}x{HALF_SIZE[1]}")
    root.resizable(False, False)

    # Welcome popup
    def show_welcome():
        # Check if the welcome message has already been shown
        temp_dir = os.path.join(os.getenv("TEMP"), "cfg.txt")
        if os.path.exists(temp_dir):
            with open(temp_dir, "r") as f:
                if f.read() == "1":
                    return

        messagebox.showinfo("Hoşgeldiniz", "Ilk defa kullaniyorsaniz, ilk taramada biraz bekleyebilirsiniz!")
        # Set a flag to indicate that the message has been shown
        # Create a file to store the flag on temp directory
        
        if not os.path.exists(temp_dir):
            with open(temp_dir, "w") as f:
                f.write("1")
        else:
            # If the file exists, it means the message has already been shown
            return

    root.after(100, show_welcome)

    # Layout
    frm = ttk.Frame(root)
    frm.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    ttk.Label(frm, text="by Mehmet C. Aksoy 2022-2025").pack(pady=2)

    def open_donate():
        wbopen("https://www.buymeacoffee.com/mcagriaksoy")
    
    # Use Buy Me A Coffee button image and wrap it in a button
    bmc_image = tk.PhotoImage(file="default-green.png", master=frm)
    # Resize the image to fit the button
    bmc_image = bmc_image.subsample(2, 2)  # Adjust (2, 2) as needed
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("BMC.TButton", relief="flat", borderwidth=0)
    btn_donate = ttk.Button(frm, image=bmc_image, command=open_donate, style="BMC.TButton")
    btn_donate.image = bmc_image  # Prevent garbage collection
    btn_donate.pack(pady=2)

    # --- Fix: Use a sub-frame for the top row of buttons ---
    top_btn_frame = ttk.Frame(frm)
    top_btn_frame.pack(fill=tk.X, pady=2)
    btn_tcdd = ttk.Button(top_btn_frame, text="TCDD Sitesine git!", width=20)
    btn_help = ttk.Button(top_btn_frame, text="Yardım", width=20)
    btn_tcdd.pack(side=tk.LEFT, padx=2)
    btn_help.pack(side=tk.LEFT, padx=2)
    # -------------------------------------------------------

    # Nereden/Nereye
    nereden_var = tk.StringVar(value="Eskişehir")
    nereye_var = tk.StringVar(value="Ankara Gar")
    ttk.Label(frm, text="Nereden :").pack(anchor="w")
    cmb_nereden = ttk.Combobox(frm, values=Sehirler.sehir_listesi, textvariable=nereden_var)
    cmb_nereden.pack(fill=tk.X)
    ttk.Label(frm, text="Nereye :").pack(anchor="w")
    cmb_nereye = ttk.Combobox(frm, values=Sehirler.sehir_listesi, textvariable=nereye_var)
    cmb_nereye.pack(fill=tk.X)

    # Bilet türü
    ttk.Label(frm, text="Arama yapılacak bilet türünü seçiniz:").pack(anchor="w")
    # Ekonomi ve Business
    ekonomi_var = tk.BooleanVar(value=True)
    business_var = tk.BooleanVar(value=False)

    check_frame = ttk.Frame(frm)
    check_frame.pack(anchor="w")
    ttk.Checkbutton(check_frame, text="Ekonomi", variable=ekonomi_var).pack(side=tk.LEFT, anchor="w")
    ttk.Checkbutton(check_frame, text="Business", variable=business_var).pack(side=tk.LEFT, anchor="w")

    # Takvim ve saat
    tarih_var = tk.StringVar(value=currentDate)
    saat_var = tk.StringVar(value=currentTime)

    def set_today():
        tarih_var.set(currentDate)

    date_frame = ttk.Frame(frm)
    date_frame.pack(anchor="w")
    
    # Takvim ve saat ayni satirda
    ttk.Label(date_frame, text="Tarih:").pack(side=tk.LEFT)
    date_entry = DateEntry(date_frame, textvariable=tarih_var, date_pattern="dd.MM.yyyy", width=10)
    date_entry.pack(side=tk.LEFT, padx=5)
    ttk.Button(date_frame, text="Bugün", command=set_today).pack(side=tk.LEFT, padx=5)
    ttk.Label(date_frame, text="Saat:").pack(side=tk.LEFT)
    ttk.Entry(date_frame, textvariable=saat_var, width=10).pack(side=tk.LEFT, padx=5)
    ttk.Label(date_frame, text="Örnek: 12:30").pack(side=tk.LEFT, padx=5)

    # Add seperator
    ttk.Separator(frm, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

    # Arama sıklığı
    ttk.Label(frm, text="Arama Sıklığını seçiniz:").pack(anchor="w")
    delay_time_var = tk.IntVar(value=1)
    ttk.Scale(frm, from_=1, to=30, orient=tk.HORIZONTAL, variable=delay_time_var).pack(fill=tk.X)

    # Update scale value on change through a label
    delay_time_label = ttk.Label(frm, text=f"{delay_time_var.get()} dakika")
    delay_time_label.pack(anchor="w")
    def update_delay_time_label(value):
        delay_time_label.config(text=f"{int(float(value))} dakika")
    delay_time_var.trace_add("write", lambda *args: update_delay_time_label(delay_time_var.get()))
    delay_time_label.bind("<Button-1>", lambda e: simpledialog.askinteger("Arama Sıklığı", "Arama sıklığını seçiniz (dakikada bir):", initialvalue=delay_time_var.get(), minvalue=1, maxvalue=30, parent=frm))


    # Telegram
    telegram_msg_var = tk.BooleanVar(value=False)
    ttk.Label(frm, text="Telegram Ayarlari: (Opsiyonel)").pack(anchor="w")
    ttk.Checkbutton(frm, text="Bilet bulunursa telegram mesaji gönder!", variable=telegram_msg_var).pack(anchor="w")
    bot_token_var = tk.StringVar()
    chat_id_var = tk.StringVar()
    ttk.Label(frm, text="Telegram Bot Token:").pack(anchor="w")
    bot_token_entry = ttk.Entry(frm, textvariable=bot_token_var, width=30).pack(anchor="w")
    ttk.Label(frm, text="Telegram Chat ID:").pack(anchor="w")
    chat_id_entry = ttk.Entry(frm, textvariable=chat_id_var, width=30).pack(anchor="w")


    # Ses
    ses_var = tk.BooleanVar(value=True)
    ttk.Label(frm, text="Ses Ayarlari: (Opsiyonel)").pack(anchor="w")
    ttk.Checkbutton(frm, text="Bilet bulunursa ses çal!", variable=ses_var).pack(anchor="w")

    # --- Fix: Use a sub-frame for the bottom row of buttons ---
    bottom_btn_frame = ttk.Frame(frm)
    bottom_btn_frame.pack(fill=tk.X, pady=2)
    btn_start = ttk.Button(bottom_btn_frame, text="Aramaya Başla")
    btn_stop = ttk.Button(bottom_btn_frame, text="Durdur!", state=tk.DISABLED)
    btn_close = ttk.Button(bottom_btn_frame, text="Kapat!", command=root.destroy)
    btn_toggle = ttk.Button(bottom_btn_frame, text="↓")
    btn_start.pack(side=tk.LEFT, padx=2)
    btn_stop.pack(side=tk.LEFT, padx=2)
    btn_close.pack(side=tk.LEFT, padx=2)
    btn_toggle.pack(side=tk.LEFT, padx=2)
    # ---------------------------------------------------------

    # Log
    log_text = ScrolledText(frm, width=32, height=8, state=tk.NORMAL)
    log_text.pack(fill=tk.BOTH, expand=True, pady=5)

    # Event handlers
    def on_start():
        nereden = nereden_var.get()
        nereye = nereye_var.get()
        tarih = tarih_var.get()
        saat = saat_var.get()
        business = business_var.get()
        ekonomi = ekonomi_var.get()
        if not saat:
            messagebox.showwarning("Uyarı", "Lütfen saat bilgisini giriniz!")
            return
        if not tarih:
            messagebox.showwarning("Uyarı", "Lütfen tarih bilgisini giriniz!")
            return
        if nereden == nereye:
            messagebox.showwarning("Uyarı", "Nereden ve Nereye aynı olamaz!")
            return
        if not (business or ekonomi):
            messagebox.showwarning("Uyarı", "Lütfen bilet türünü seçiniz!")
            return
        if "/" in tarih:
            tarih = tarih.replace("/", ".")
        elif "-" in tarih:
            tarih = tarih.replace("-", ".")
        if "." in saat:
            saat = saat.replace(".", ":")
        elif "," in saat:
            saat = saat.replace(",", ":")
        delay_time = delay_time_var.get()
        telegram_msg = telegram_msg_var.get()
        if telegram_msg:
            if not bot_token_var.get() or not chat_id_var.get():
                messagebox.showwarning("Uyarı", "Telegram bot token ve chat id bilgilerini giriniz!")
                return
        bot_token = bot_token_var.get()
        if bot_token and not TelegramMsg.TelegramMsg().check_telegram_bot_status(bot_token):
            messagebox.showwarning("Uyarı", "Telegram bot token bilgisi hatali! kontrol ediniz!")
            return
        chat_id = chat_id_var.get()
        ses = ses_var.get()
        btn_start.config(state=tk.DISABLED)
        btn_stop.config(state=tk.NORMAL)
        log_text.insert(tk.END, "Arama başladı. Lütfen bekleyin...\n")
        def thread1(delay_time, telegram_msg, bot_token, chat_id, ses):
            global g_isStopped
            g_isStopped = False
            while True:
                driver = driver_setting()
                driver_get(driver)
                route(driver, nereden, nereye, tarih)
                control(driver, saat, delay_time, telegram_msg, bot_token, chat_id, ses)
                sleep(30)
        t1 = Thread(target=thread1, args=(delay_time, telegram_msg, bot_token, chat_id, ses))
        t1.start()

    def on_stop():
        btn_start.config(state=tk.NORMAL)
        btn_stop.config(state=tk.DISABLED)
        global g_isStopped
        g_isStopped = True
        log_text.delete(1.0, tk.END)

    def on_help():
        if messagebox.askyesno("Yardım", "Yardım sayfasına gitmek ister misiniz?"):
            wbopen("https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol")

    def on_tcdd():
        messagebox.showinfo("Bilgi", "TCDD Bilet Satış Sitesine yönlendiriliyorsunuz. Lütfen bekleyin...")
        wbopen("https://ebilet.tcddtasimacilik.gov.tr")

    def on_toggle():
        if root.geometry().startswith(f"{FULL_SIZE[0]}x{FULL_SIZE[1]}"):
            btn_toggle.config(text="↓")
            root.geometry(f"{HALF_SIZE[0]}x{HALF_SIZE[1]}")
        else:
            btn_toggle.config(text="↑")
            root.geometry(f"{FULL_SIZE[0]}x{FULL_SIZE[1]}")

    btn_start.config(command=on_start)
    btn_stop.config(command=on_stop)
    btn_help.config(command=on_help)
    btn_tcdd.config(command=on_tcdd)
    btn_toggle.config(command=on_toggle)

    root.mainloop()

def __main__():
    main()
