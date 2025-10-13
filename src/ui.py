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
from tkinter import ttk, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
from tkcalendar import DateEntry
from selenium.common.exceptions import InvalidSessionIdException

import error_codes as ErrCodes
from webbrowser import open as wbopen

if platform.system() == "Windows":
    import winsound
    try:
        from win10toast import ToastNotifier
        toast_available = True
    except ImportError:
        toast_available = False
else:
    toast_available = False

import Control
import DriverGet
import DriverSetting
import Sehirler
import Rota
import TelegramMsg

g_isStopped = False

FULL_SIZE = (540, 760)
HALF_SIZE = (540, 560)


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
        if isError == -1 or g_isStopped:
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
            
            # Show Windows toast notification if available
            if toast_available:
                try:
                    toaster = ToastNotifier()
                    toaster.show_toast(
                        "TCDD Bilet Bulundu!",
                        "Hey Orada mısın? Biletin bulundu. Satın alabilirsin ❤️",
                        icon_path=None,
                        duration=10,
                        threaded=True
                    )
                except Exception as e:
                    print(f"Failed to show toast notification: {e}")
            
            messagebox.showinfo(
                "Bilet Bulundu",
                "Hey Orada mısın? Biletin bulundu. Satın alabilirsin ❤️❤️❤️❤️",
            )
        elif response == ErrCodes.TEKRAR_DENE:
            log_text.insert(
                tk.END, f"\n{delay_time} Dakika icerisinde tekrar denenecek..."
            )
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
    root.title("TCDD Otomatik Bilet Arama (Yer Bulma) Programı - v4.0.0")
    root.resizable(False, False)

    # Center the window on screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = HALF_SIZE[0]
    window_height = HALF_SIZE[1]
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # Bind Escape key to close window
    root.bind('<Escape>', lambda e: root.destroy())

    # Apply modern theme
    style = ttk.Style()
    style.theme_use('clam')

    # Configure modern styling
    style.configure('TFrame', background='#f8f9fa')
    style.configure('TLabel', background='#f8f9fa', font=('Segoe UI', 9))
    style.configure('TButton', font=('Segoe UI', 9, 'bold'), padding=6, relief='raised', borderwidth=1)
    style.configure('TCheckbutton', background='#f8f9fa', font=('Segoe UI', 9))
    style.configure('TCombobox', font=('Segoe UI', 9))
    style.configure('TEntry', font=('Segoe UI', 9))
    style.configure('Card.TLabelframe', background='#ffffff', borderwidth=2, relief='solid', labeloutside=False)
    style.configure('Card.TLabelframe.Label', background='#ffffff', font=('Segoe UI', 10, 'bold'), foreground='#2c3e50')

    # Button colors and styles
    style.map('TButton',
        background=[('active', '#007bff'), ('pressed', '#0056b3')],
        foreground=[('active', 'white'), ('pressed', 'white')]
    )

    # Start button - green
    style.configure('Start.TButton', background='#28a745', foreground='white', font=('Segoe UI', 10, 'bold'))
    style.map('Start.TButton',
        background=[('active', '#218838'), ('pressed', '#1e7e34')],
        foreground=[('active', 'white'), ('pressed', 'white')]
    )

    # Stop button - red
    style.configure('Stop.TButton', background='#dc3545', foreground='white', font=('Segoe UI', 10, 'bold'))
    style.map('Stop.TButton',
        background=[('active', '#c82333'), ('pressed', '#bd2130')],
        foreground=[('active', 'white'), ('pressed', 'white')]
    )

    # Close button - gray
    style.configure('Close.TButton', background='#6c757d', foreground='white', font=('Segoe UI', 9))
    style.map('Close.TButton',
        background=[('active', '#5a6268'), ('pressed', '#545b62')],
        foreground=[('active', 'white'), ('pressed', 'white')]
    )

    # Disabled button style - gray for disabled state
    style.configure('Disabled.TButton', background='#cccccc', foreground='#666666', font=('Segoe UI', 9, 'bold'))
    style.map('Disabled.TButton',
        background=[('active', '#cccccc'), ('pressed', '#cccccc')],
        foreground=[('active', '#666666'), ('pressed', '#666666')]
    )

    # Welcome popup
    def show_welcome():
        # Check if the welcome message has already been shown
        temp_dir = os.path.join(os.getenv("TEMP"), "cfg.txt")
        if os.path.exists(temp_dir):
            with open(temp_dir, "r") as f:
                if f.read() == "1":
                    return

        messagebox.showinfo(
            "Hoşgeldiniz",
            "Ilk defa kullaniyorsaniz, ilk taramada biraz bekleyebilirsiniz!",
        )
        # Set a flag to indicate that the message has been shown
        # Create a file to store the flag on temp directory

        if not os.path.exists(temp_dir):
            with open(temp_dir, "w") as f:
                f.write("1")
        else:
            # If the file exists, it means the message has already been shown
            return

    root.after(100, show_welcome)

    # Main container with modern background
    main_frame = ttk.Frame(root, style='TFrame')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

    # Header section with title and donate button
    header_frame = ttk.Frame(main_frame, style='TFrame')
    header_frame.pack(fill=tk.X, pady=(0, 15))

    # Title and controls on the same line
    title_frame = ttk.Frame(header_frame, style='TFrame')
    title_frame.pack(fill=tk.X)

    # Create main grid container
    content_frame = ttk.Frame(main_frame, style='TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Configure grid weights for responsive layout
    content_frame.grid_columnconfigure(0, weight=1)  # Left column
    content_frame.grid_columnconfigure(1, weight=1)  # Right column
    content_frame.grid_rowconfigure(0, weight=0)     # Route section
    content_frame.grid_rowconfigure(1, weight=0)     # Ticket type / Date time section
    content_frame.grid_rowconfigure(2, weight=0)     # Settings / Controls section
    content_frame.grid_rowconfigure(3, weight=0)     # Author text
    content_frame.grid_rowconfigure(4, weight=1)     # Log section (expands)

    # Route selection section (Top Left)
    route_frame = ttk.Frame(content_frame, style='TFrame', relief='solid', borderwidth=1)
    route_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    # Nereden/Nereye
    nereden_var = tk.StringVar(value="Eskişehir")
    nereye_var = tk.StringVar(value="Ankara Gar")
    ttk.Label(route_frame, text="🚂 Rota Seçimi", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))

    # Use an inner frame with grid to align label and combobox on the same row
    route_inner = ttk.Frame(route_frame, style='TFrame')
    route_inner.pack(padx=10, pady=(0, 10), fill='x')

    ttk.Label(route_inner, text="Nereden:").grid(row=0, column=0, sticky='w', padx=(0, 5), pady=2)
    cmb_nereden = ttk.Combobox(route_inner, values=Sehirler.sehir_listesi, textvariable=nereden_var, width=20)
    cmb_nereden.grid(row=0, column=1, sticky='ew', pady=2)

    ttk.Label(route_inner, text="Nereye:").grid(row=1, column=0, sticky='w', padx=(0, 5), pady=2)
    cmb_nereye = ttk.Combobox(route_inner, values=Sehirler.sehir_listesi, textvariable=nereye_var, width=20)
    cmb_nereye.grid(row=1, column=1, sticky='ew', pady=2)

    # Allow the combobox column to expand for better alignment
    route_inner.grid_columnconfigure(1, weight=1)

    # Ticket type section (Top Right)
    ticket_frame = ttk.Frame(content_frame, style='TFrame', relief='solid', borderwidth=1)
    ticket_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

    # Bilet türü
    ekonomi_var = tk.BooleanVar(value=True)
    business_var = tk.BooleanVar(value=False)
    ttk.Label(ticket_frame, text="🎫 Bilet Türü", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
    ttk.Label(ticket_frame, text="Arama yapılacak bilet türünü seçiniz:").pack(pady=(0, 5))
    check_frame = ttk.Frame(ticket_frame)
    check_frame.pack(pady=(0, 10))
    ttk.Checkbutton(check_frame, text="Ekonomi", variable=ekonomi_var).pack(side=tk.LEFT, padx=(0, 20))
    ttk.Checkbutton(check_frame, text="Business", variable=business_var).pack(side=tk.LEFT)

    # Date and time section (Middle Left)
    datetime_frame = ttk.Frame(content_frame, style='TFrame', relief='solid', borderwidth=1)
    datetime_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

    # Takvim ve saat
    tarih_var = tk.StringVar(value=currentDate)
    saat_var = tk.StringVar(value=currentTime)

    def set_today():
        tarih_var.set(currentDate)

    ttk.Label(datetime_frame, text="📅 Tarih ve Saat", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
    date_frame = ttk.Frame(datetime_frame)
    date_frame.pack(pady=(0, 10))
    ttk.Label(date_frame, text="Tarih:").grid(row=0, column=0, sticky='w', padx=(0, 5))
    date_entry = DateEntry(date_frame, textvariable=tarih_var, date_pattern="dd.MM.yyyy", width=12)
    date_entry.grid(row=0, column=1, padx=(0, 10))
    ttk.Button(date_frame, text="Bugün", command=set_today).grid(row=0, column=2)
    ttk.Label(date_frame, text="Saat:").grid(row=1, column=0, sticky='w', padx=(0, 5), pady=(5, 0))
    ttk.Entry(date_frame, textvariable=saat_var, width=12).grid(row=1, column=1, padx=(0, 10), pady=(5, 0))
    ttk.Label(date_frame, text="Örnek: 12:30").grid(row=1, column=2, pady=(5, 0))

    # Search frequency section (Middle Right)
    frequency_frame = ttk.Frame(content_frame, style='TFrame', relief='solid', borderwidth=1)
    frequency_frame.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

    # Arama sıklığı
    delay_time_var = tk.IntVar(value=1)
    ttk.Label(frequency_frame, text="⏱️ Arama Sıklığı", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
    ttk.Label(frequency_frame, text="Arama sıklığını seçiniz:").pack(pady=(0, 5))
    ttk.Scale(frequency_frame, from_=1, to=30, orient=tk.HORIZONTAL, variable=delay_time_var).pack(fill=tk.X, padx=10, pady=(0, 5))
    delay_time_label = ttk.Label(frequency_frame, text=f"{delay_time_var.get()} dakika")
    delay_time_label.pack(pady=(0, 10))

    def update_delay_time_label(value):
        delay_time_label.config(text=f"{int(float(value))} dakika")

    delay_time_var.trace_add(
        "write", lambda *args: update_delay_time_label(delay_time_var.get())
    )
    delay_time_label.bind(
        "<Button-1>",
        lambda e: simpledialog.askinteger(
            "Arama Sıklığı",
            "Arama sıklığını seçiniz (dakikada bir):",
            initialvalue=delay_time_var.get(),
            minvalue=1,
            maxvalue=30,
            parent=frequency_frame,
        ),
    )

    # Settings section (Bottom Left)
    settings_frame = ttk.Frame(content_frame, style='TFrame', relief='solid', borderwidth=1)
    settings_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)

    # Telegram and sound settings
    telegram_msg_var = tk.BooleanVar(value=False)
    bot_token_var = tk.StringVar()
    chat_id_var = tk.StringVar()
    ses_var = tk.BooleanVar(value=True)

    ttk.Label(settings_frame, text="📢 Bildirim Ayarları", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))

    # Telegram settings
    ttk.Label(settings_frame, text="Telegram (Opsiyonel):").pack(anchor="w", padx=10, pady=(5, 2))
    ttk.Checkbutton(settings_frame, text="Bilet bulunursa mesaj gönder", variable=telegram_msg_var).pack(anchor="w", padx=20)
    ttk.Label(settings_frame, text="Bot Token:").pack(anchor="w", padx=10, pady=(5, 2))
    bot_token_entry = ttk.Entry(settings_frame, textvariable=bot_token_var, width=25)
    bot_token_entry.pack(padx=10, pady=(0, 5))
    ttk.Label(settings_frame, text="Chat ID:").pack(anchor="w", padx=10, pady=(5, 2))
    chat_id_entry = ttk.Entry(settings_frame, textvariable=chat_id_var, width=25)
    chat_id_entry.pack(padx=10, pady=(0, 10))

    # Sound settings
    ttk.Label(settings_frame, text="Ses (Opsiyonel):").pack(anchor="w", padx=10, pady=(5, 2))
    ttk.Checkbutton(settings_frame, text="Bilet bulunursa ses çal", variable=ses_var).pack(anchor="w", padx=20, pady=(0, 10))

    # Control buttons section (Bottom Right)
    control_frame = ttk.Frame(content_frame, style='TFrame', relief='solid', borderwidth=1)
    control_frame.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)

    ttk.Label(control_frame, text="🎮 Kontrol Paneli", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 10))

    # Main control buttons
    main_buttons_frame = ttk.Frame(control_frame, style='TFrame')
    main_buttons_frame.pack(pady=(0, 10))
    btn_start = ttk.Button(main_buttons_frame, text="🔍 Başla", style='Start.TButton', width=12)
    btn_stop = ttk.Button(main_buttons_frame, text="⏹️ Durdur", state=tk.DISABLED, style='Stop.TButton', width=10)
    btn_start.pack(side=tk.LEFT, padx=5)
    btn_stop.pack(side=tk.LEFT, padx=5)

    # Action buttons
    action_buttons_frame = ttk.Frame(control_frame, style='TFrame')
    action_buttons_frame.pack(pady=(0, 10))
    btn_tcdd = ttk.Button(action_buttons_frame, text="🌐 TCDD Sitesi", width=12)
    btn_help = ttk.Button(action_buttons_frame, text="❓ Yardım", width=10)

    btn_tcdd.pack(side=tk.LEFT, padx=5)
    btn_help.pack(side=tk.LEFT, padx=5)

    
    # Secondary buttons
    secondary_buttons_frame = ttk.Frame(control_frame, style='TFrame')
    secondary_buttons_frame.pack(pady=(0, 10))
    btn_toggle = ttk.Button(secondary_buttons_frame, text="🔄 LOG'ları göster", width=15, style='TButton')
    btn_close = ttk.Button(secondary_buttons_frame, text="❌ Kapat", command=root.destroy, style='Close.TButton', width=10)
    btn_close.pack(side=tk.LEFT, padx=5)
    btn_toggle.pack(side=tk.LEFT, padx=5)

    # Donate button on separate line
    def open_donate():
        wbopen("https://www.buymeacoffee.com/mcagriaksoy")

    donate_frame = ttk.Frame(control_frame, style='TFrame')
    donate_frame.pack(pady=(0, 10))

    try:
        bmc_image = tk.PhotoImage(file="donate.jpg", master=donate_frame)
        bmc_image = bmc_image.subsample(2, 2)  # Smaller size
        style.configure("BMC.TButton", relief="flat", borderwidth=0, background='#f8f9fa')
        btn_donate = ttk.Button(
            donate_frame, image=bmc_image, command=open_donate, style="BMC.TButton"
        )
        btn_donate.image = bmc_image  # Prevent garbage collection
        btn_donate.pack()
    except Exception:
        # If image not found, create a text button instead
        btn_donate = ttk.Button(
            donate_frame, text="☕ Donate", command=open_donate, style="TButton"
        )
        btn_donate.pack()

    # Author text before log section
    author_frame = ttk.Frame(content_frame, style='TFrame')
    author_frame.grid(row=3, column=0, columnspan=2, sticky='ew', padx=5, pady=(10, 5))
    # Loader (hidden by default) - placed before the author text to indicate background processing
    loader_frame = ttk.Frame(author_frame, style='TFrame')
    loader_frame.pack(side=tk.TOP, fill='x')
    loader = ttk.Progressbar(loader_frame, mode='indeterminate')
    # Don't pack the loader yet; it'll be packed when active

    author_label = ttk.Label(author_frame, text="Mehmet C. Aksoy 2022-2025 Tarafından Geliştirildi. Tüm hakları saklıdır.",
                            font=('Segoe UI', 8), foreground='#6c757d')
    author_label.pack(anchor='center')

    # Log section (Full width bottom)
    log_frame = ttk.Frame(content_frame, style='TFrame', relief='solid', borderwidth=1)
    log_frame.grid(row=4, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

    ttk.Label(log_frame, text="📋 Arama Logları", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
    log_text = ScrolledText(log_frame, height=8, state=tk.NORMAL, font=('Consolas', 9))
    log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    # Thread-safe GUI logging helper
    def gui_log(msg):
        try:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            root.after(0, lambda: log_text.insert(tk.END, f"[{ts}] {msg}\n"))
            root.after(0, lambda: log_text.see(tk.END))
        except Exception:
            # best-effort, do not crash background thread
            pass

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
                messagebox.showwarning(
                    "Uyarı", "Telegram bot token ve chat id bilgilerini giriniz!"
                )
                return
        bot_token = bot_token_var.get()
        if bot_token and not TelegramMsg.TelegramMsg().check_telegram_bot_status(
            bot_token
        ):
            messagebox.showwarning(
                "Uyarı", "Telegram bot token bilgisi hatali! kontrol ediniz!"
            )
            return
        chat_id = chat_id_var.get()
        ses = ses_var.get()
        btn_start.config(state=tk.DISABLED, style='Disabled.TButton')
        btn_stop.config(state=tk.NORMAL, style='Stop.TButton')
        gui_log("Arama başladı. Lütfen bekleyin...")

        # Show and start the loader in a thread-safe way
        def _show_loader():
            try:
                loader.pack(fill='x', padx=5, pady=(0, 5))
                loader.start(10)
            except Exception:
                pass

        root.after(0, _show_loader)

        def thread1(delay_time, telegram_msg, bot_token, chat_id, ses):
            global g_isStopped
            g_isStopped = False
            attempt = 0
            while True:
                if g_isStopped:
                    gui_log("Kullanıcı tarafından durduruldu (döngü başlangıcında).")
                    break
                attempt += 1
                gui_log(f"Başlangıç döngüsü: deneme #{attempt}")
                driver = driver_setting()
                if driver is None:
                    gui_log("HATA: Tarayıcı başlatılamadı! Lütfen Edge tarayıcısının yüklü olduğundan emin olun.")
                    btn_start.config(state=tk.NORMAL)
                    btn_stop.config(state=tk.DISABLED)
                    break

                if g_isStopped:
                    gui_log("Durduruldu (sayfa yüklemeden önce).")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    break
                # driver_get with exception handling
                try:
                    gui_log("Sayfa yükleme başlıyor...")
                    driver_get(driver)
                    gui_log("Sayfa yüklendi başarılı.")
                except InvalidSessionIdException as ise:
                    gui_log(f"InvalidSessionIdException during driver_get: {ise}")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    break  # Kill the thread on exception
                except Exception as e:
                    gui_log(f"Hata: sayfa yüklenemedi: {e}")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    break  # Kill the thread on exception

                if g_isStopped:
                    gui_log("Durduruldu (rota girişinden önce).")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    break
                # route with exception handling
                try:
                    gui_log(f"Rota bilgileri giriliyor: {nereden} -> {nereye} {tarih}")
                    route(driver, nereden, nereye, tarih)
                    gui_log("Rota bilgileri girildi.")
                except InvalidSessionIdException as ise:
                    gui_log(f"InvalidSessionIdException during route: {ise}")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    break  # Kill the thread on exception
                except Exception as e:
                    gui_log(f"Rota işlemi sırasında hata: {e}")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    break  # Kill the thread on exception

                if g_isStopped:
                    gui_log("Durduruldu (kontrol öncesi).")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    break
                # control with exception handling
                try:
                    gui_log(f"Kontrol başlıyor: Saat={saat}, Bekleme={delay_time} dakika")
                    control(driver, saat, delay_time, telegram_msg, bot_token, chat_id, ses)
                    gui_log("Kontrol tamamlandı.")
                except InvalidSessionIdException as ise:
                    gui_log(f"InvalidSessionIdException during control: {ise}")
                    driver.quit()
                except Exception as e:
                    gui_log(f"Kontrol sırasında hata: {e}")
                    driver.quit()

                gui_log(f"Bekleniyor: {delay_time} dakika sonra tekrar denenecek.")
                # Replace single sleep with loop to check g_isStopped every second
                for _ in range(delay_time * 60):
                    if g_isStopped:
                        gui_log("Bekleme sırasında durduruldu.")
                        driver.quit()
                        break
                    sleep(1)

            # When the background loop exits (either stopped or finished), stop the loader and restore buttons
            def _hide_loader_and_restore():
                try:
                    loader.stop()
                    loader.pack_forget()
                except Exception:
                    pass
                btn_start.config(state=tk.NORMAL)
                btn_stop.config(state=tk.DISABLED)

            root.after(0, _hide_loader_and_restore)

        t1 = Thread(
            target=thread1, args=(delay_time, telegram_msg, bot_token, chat_id, ses)
        )
        t1.start()

    def on_stop():
        btn_start.config(state=tk.NORMAL, style='Start.TButton')
        btn_stop.config(state=tk.DISABLED, style='Disabled.TButton')
        global g_isStopped
        g_isStopped = True
        log_text.delete(1.0, tk.END)
        # Hide and stop loader when user presses stop
        try:
            loader.stop()
            loader.pack_forget()
        except Exception:
            pass

    def on_help():
        if messagebox.askyesno("Yardım", "Yardım sayfasına gitmek ister misiniz?"):
            wbopen("https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol")

    def on_tcdd():
        messagebox.showinfo(
            "Bilgi",
            "TCDD Bilet Satış Sitesine yönlendiriliyorsunuz. Lütfen bekleyin...",
        )
        wbopen("https://ebilet.tcddtasimacilik.gov.tr")

    def on_toggle():
        if root.geometry().startswith(f"{FULL_SIZE[0]}x{FULL_SIZE[1]}"):
            btn_toggle.config(text="🔄 Genişlet/Daralt")
            root.geometry(f"{HALF_SIZE[0]}x{HALF_SIZE[1]}")
        else:
            btn_toggle.config(text="🔄 Genişlet/Daralt")
            root.geometry(f"{FULL_SIZE[0]}x{FULL_SIZE[1]}")

    btn_start.config(command=on_start)
    btn_stop.config(command=on_stop)
    btn_help.config(command=on_help)
    btn_tcdd.config(command=on_tcdd)
    btn_toggle.config(command=on_toggle)

    root.mainloop()


def __main__():
    main()
