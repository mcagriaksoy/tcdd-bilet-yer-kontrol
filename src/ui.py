# -*- coding: utf-8 -*-
"""
Base version @author: Birol Emekli, https://github.com/bymcs
Enhanced (Forked) version @author: Mehmet C. Aksoy https://github.com/mcagriaksoy
"""

import json
import os
import platform
import re
import sys
import tkinter as tk
from datetime import date, datetime
from threading import Thread
from time import sleep
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from webbrowser import open as wbopen

from selenium.common.exceptions import InvalidSessionIdException
from tkcalendar import DateEntry

import Control
import DriverGet
import DriverSetting
import Rota
import Sehirler
import TelegramMsg
import error_codes as ErrCodes

if platform.system() == "Windows":
    import winsound

    try:
        from win10toast import ToastNotifier

        toast_available = True
    except ImportError:
        toast_available = False
else:
    toast_available = False

GITHUB_RELEASES_URL = "https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/releases"
GITHUB_LATEST_API = (
    "https://api.github.com/repos/mcagriaksoy/tcdd-bilet-yer-kontrol/releases/latest"
)
APP_SIZE = (980, 820)
COMPACT_SIZE = (980, 660)
APP_BG = "#eef3f8"
CARD_BG = "#ffffff"
ACCENT = "#0f5f9c"
ACCENT_SOFT = "#d9ebf8"
TEXT_MAIN = "#17324d"
TEXT_MUTED = "#5d7186"
DANGER = "#b54646"
BORDER = "#d4dee8"

g_isStopped = False


def resource_path(*parts):
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, *parts)


def read_current_version():
    version_file = os.path.join(os.getcwd(), "version.txt")
    try:
        with open(version_file, "r", encoding="utf-8") as file:
            content = file.read()
        match = re.search(r"FileVersion',\s*'([^']+)'", content)
        if match:
            return match.group(1)
    except OSError:
        pass
    return "4.0.0"


def parse_version_tuple(raw_version):
    numbers = [int(piece) for piece in re.findall(r"\d+", raw_version)]
    return tuple(numbers[:4]) if numbers else (0,)


def fetch_latest_release_info():
    request = Request(
        GITHUB_LATEST_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "tcdd-bilet-yer-kontrol",
        },
    )
    with urlopen(request, timeout=8) as response:
        payload = json.loads(response.read().decode("utf-8"))

    tag_name = payload.get("tag_name", "").strip() or "Bilinmiyor"
    return {
        "tag_name": tag_name,
        "version": ".".join(re.findall(r"\d+", tag_name)) or tag_name,
        "html_url": payload.get("html_url", GITHUB_RELEASES_URL),
        "published_at": payload.get("published_at", ""),
    }


def center_geometry(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - width) / 2)
    center_y = int((screen_height - height) / 2)
    root.geometry(f"{width}x{height}+{center_x}+{center_y}")


def main():
    current_version = read_current_version()

    def driver_setting():
        return DriverSetting.DriverSetting().driver_init()

    def driver_get(drivers):
        DriverGet.DriverGet(drivers).driver_get()

    def route(driver, first_location, last_location, date_):
        global g_isStopped
        is_error = Rota.Rota(driver, first_location, last_location, date_).dataInput()
        if is_error == -1 or g_isStopped:
            safe_driver_quit(driver)
            return False
        return True

    def control(
        driver,
        time_text,
        delay_time,
        telegram_msg,
        bot_token,
        chat_id,
        ses,
        allow_economy,
        allow_business,
    ):
        response = Control.Control(
            driver,
            time_text,
            allow_economy=allow_economy,
            allow_business=allow_business,
        ).sayfa_kontrol()
        if response == ErrCodes.BASARILI:
            if ses:
                play_sound()
            if telegram_msg:
                sent = TelegramMsg.TelegramMsg().send_telegram_message(bot_token, chat_id)
                if not sent:
                    append_log("Telegram bildirimi gönderilemedi.")

            show_toast_notification()
            safe_driver_quit(driver)
            root.after(
                0,
                lambda: messagebox.showinfo(
                    "Bilet Bulundu",
                    "Bilet bulundu. TCDD sitesine gidip satın alma işlemini tamamlayabilirsiniz.",
                ),
            )
        elif response == ErrCodes.TEKRAR_DENE:
            append_log(f"{delay_time} dakika sonra tekrar denenecek.")
            safe_driver_quit(driver)
        elif response == ErrCodes.TIMEOUT_HATASI:
            safe_driver_quit(driver)
        else:
            safe_driver_quit(driver)
        return response

    def play_sound():
        if platform.system() != "Windows":
            return
        try:
            for _ in range(4):
                winsound.Beep(1100, 350)
                sleep(0.1)
        except Exception:
            append_log("Ses bildirimi çalınamadı.")

    def show_toast_notification():
        if not toast_available:
            return
        try:
            toaster = ToastNotifier()
            toaster.show_toast(
                "TCDD Bilet Bulundu",
                "Bilet bulundu. Satın alma işlemini tamamlayabilirsiniz.",
                duration=8,
                threaded=True,
            )
        except Exception:
            append_log("Masaüstü bildirimi gösterilemedi.")

    def safe_driver_quit(driver):
        if not driver:
            return
        try:
            driver.quit()
        except Exception:
            pass

    def normalize_date_text(raw_text):
        return raw_text.replace("/", ".").replace("-", ".").strip()

    def normalize_time_text(raw_text):
        return raw_text.replace(".", ":").replace(",", ":").strip()

    def validate_form():
        nereden = nereden_var.get().strip()
        nereye = nereye_var.get().strip()
        tarih = normalize_date_text(tarih_var.get())
        saat = normalize_time_text(saat_var.get())
        allow_business = business_var.get()
        allow_economy = ekonomi_var.get()

        if not nereden or not nereye:
            raise ValueError("Lütfen kalkış ve varış istasyonlarını seçin.")
        if nereden == nereye:
            raise ValueError("Kalkış ve varış istasyonları aynı olamaz.")
        if not (allow_business or allow_economy):
            raise ValueError("En az bir bilet tipi seçin.")
        if not tarih:
            raise ValueError("Lütfen tarih seçin.")
        if not saat:
            raise ValueError("Lütfen saat girin.")

        try:
            datetime.strptime(tarih, "%d.%m.%Y")
        except ValueError as exc:
            raise ValueError("Tarih formatı gg.aa.yyyy olmalı.") from exc

        try:
            datetime.strptime(saat, "%H:%M")
        except ValueError as exc:
            raise ValueError("Saat formatı ss:dd olmalı. Örnek: 12:30") from exc

        if telegram_msg_var.get():
            if not bot_token_var.get().strip() or not chat_id_var.get().strip():
                raise ValueError("Telegram için bot token ve chat id bilgilerini girin.")
            if not TelegramMsg.TelegramMsg().check_telegram_bot_status(
                bot_token_var.get().strip()
            ):
                raise ValueError("Telegram bot token bilgisi doğrulanamadı.")

        return {
            "nereden": nereden,
            "nereye": nereye,
            "tarih": tarih,
            "saat": saat,
            "delay_time": int(delay_time_var.get()),
            "telegram_msg": telegram_msg_var.get(),
            "bot_token": bot_token_var.get().strip(),
            "chat_id": chat_id_var.get().strip(),
            "ses": ses_var.get(),
            "allow_business": allow_business,
            "allow_economy": allow_economy,
        }

    root = tk.Tk()
    root.title(f"TCDD Otomatik Bilet Arama Botu")
    root.configure(bg=APP_BG)
    root.resizable(False, False)
    try:
        root.iconbitmap(resource_path("icon.ico"))
    except tk.TclError:
        pass
    center_geometry(root, *APP_SIZE)
    root.bind("<Escape>", lambda _event: root.destroy())

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(".", background=APP_BG, foreground=TEXT_MAIN, font=("Segoe UI", 10))
    style.configure("App.TFrame", background=APP_BG)
    style.configure("CardInner.TFrame", background=CARD_BG)
    style.configure(
        "Card.TLabelframe",
        background=CARD_BG,
        bordercolor=BORDER,
        relief="solid",
        borderwidth=1,
        padding=14,
    )
    style.configure(
        "Card.TLabelframe.Label",
        background=CARD_BG,
        foreground=TEXT_MAIN,
        font=("Segoe UI Semibold", 11),
    )
    style.configure(
        "Title.TLabel",
        background=APP_BG,
        foreground=TEXT_MAIN,
        font=("Segoe UI Semibold", 21),
    )
    style.configure(
        "Muted.TLabel",
        background=APP_BG,
        foreground=TEXT_MUTED,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Section.TLabel",
        background=CARD_BG,
        foreground=TEXT_MUTED,
        font=("Segoe UI", 9),
    )
    style.configure(
        "CardText.TLabel",
        background=CARD_BG,
        foreground=TEXT_MAIN,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Primary.TButton",
        background=ACCENT,
        foreground="white",
        borderwidth=0,
        padding=(14, 9),
        font=("Segoe UI Semibold", 10),
    )
    style.map("Primary.TButton", background=[("active", "#0d507f"), ("pressed", "#0a446c")])
    style.configure(
        "Ghost.TButton",
        background=ACCENT_SOFT,
        foreground=ACCENT,
        borderwidth=0,
        padding=(12, 8),
        font=("Segoe UI", 10),
    )
    style.map("Ghost.TButton", background=[("active", "#c8e1f3"), ("pressed", "#bdd9ee")])
    style.configure(
        "Danger.TButton",
        background=DANGER,
        foreground="white",
        borderwidth=0,
        padding=(14, 9),
        font=("Segoe UI Semibold", 10),
    )
    style.map("Danger.TButton", background=[("active", "#9e3d3d"), ("pressed", "#8d3636")])
    style.configure("TEntry", fieldbackground="#f8fbfd", bordercolor=BORDER, padding=6)
    style.configure("TCombobox", fieldbackground="#f8fbfd", padding=4)
    style.configure(
        "TCheckbutton",
        background=CARD_BG,
        foreground=TEXT_MAIN,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Status.Horizontal.TProgressbar",
        troughcolor="#dfe7ef",
        background=ACCENT,
        thickness=8,
    )

    current_date = date.today().strftime("%d.%m.%Y")
    current_time = datetime.now().strftime("%H:%M")

    nereden_var = tk.StringVar(value="Eskişehir")
    nereye_var = tk.StringVar(value="Ankara Gar")
    tarih_var = tk.StringVar(value=current_date)
    saat_var = tk.StringVar(value=current_time)
    ekonomi_var = tk.BooleanVar(value=True)
    business_var = tk.BooleanVar(value=False)
    delay_time_var = tk.IntVar(value=1)
    telegram_msg_var = tk.BooleanVar(value=False)
    bot_token_var = tk.StringVar()
    chat_id_var = tk.StringVar()
    ses_var = tk.BooleanVar(value=True)
    update_status_var = tk.StringVar(value="Sürüm bilgisi hazırlanıyor...")
    update_detail_var = tk.StringVar(value=f"Yüklü sürüm: v{current_version}")
    run_status_var = tk.StringVar(value="Hazır")
    latest_release_url = {"value": GITHUB_RELEASES_URL}

    main_frame = ttk.Frame(root, style="App.TFrame", padding=18)
    main_frame.pack(fill=tk.BOTH, expand=True)

    header_frame = ttk.Frame(main_frame, style="App.TFrame")
    header_frame.pack(fill=tk.X, pady=(0, 14))

    title_column = ttk.Frame(header_frame, style="App.TFrame")
    title_column.pack(side=tk.LEFT, fill=tk.X, expand=True)
    ttk.Label(title_column, text="TCDD Bilet Yer Kontrol", style="Title.TLabel").pack(anchor="w")
    ttk.Label(
        title_column,
        text="Daha temiz bir akış, iyileştirilmiş kontroller ve sürüm takibi tek ekranda.",
        style="Muted.TLabel",
    ).pack(anchor="w", pady=(4, 0))

    version_frame = tk.Frame(
        header_frame,
        bg=ACCENT_SOFT,
        highlightbackground="#b7d4eb",
        highlightthickness=1,
    )
    version_frame.pack(side=tk.RIGHT, padx=(16, 0), ipadx=12, ipady=8)
    tk.Label(
        version_frame,
        text=f"v{current_version}",
        bg=ACCENT_SOFT,
        fg=ACCENT,
        font=("Segoe UI Semibold", 16),
    ).pack()
    tk.Label(
        version_frame,
        text="Yüklü sürüm",
        bg=ACCENT_SOFT,
        fg=TEXT_MUTED,
        font=("Segoe UI", 9),
    ).pack()

    overview_frame = tk.Frame(
        main_frame,
        bg=CARD_BG,
        highlightbackground=BORDER,
        highlightthickness=1,
    )
    overview_frame.pack(fill=tk.X, pady=(0, 14))

    status_left = tk.Frame(overview_frame, bg=CARD_BG)
    status_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=16, pady=14)
    tk.Label(
        status_left,
        textvariable=update_status_var,
        bg=CARD_BG,
        fg=TEXT_MAIN,
        font=("Segoe UI Semibold", 12),
    ).pack(anchor="w", pady=(3, 2))
    tk.Label(
        status_left,
        textvariable=update_detail_var,
        bg=CARD_BG,
        fg=TEXT_MUTED,
        font=("Segoe UI", 10),
    ).pack(anchor="w")

    status_actions = ttk.Frame(overview_frame, style="App.TFrame")
    status_actions.pack(side=tk.RIGHT, padx=16, pady=14)

    content_frame = ttk.Frame(main_frame, style="App.TFrame")
    content_frame.pack(fill=tk.BOTH, expand=True)
    content_frame.grid_columnconfigure(0, weight=3)
    content_frame.grid_columnconfigure(1, weight=2)
    content_frame.grid_rowconfigure(2, weight=1)

    route_frame = ttk.LabelFrame(content_frame, text="Rota ve Tarih", style="Card.TLabelframe")
    route_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
    route_grid = ttk.Frame(route_frame, style="CardInner.TFrame")
    route_grid.pack(fill=tk.X)
    route_grid.grid_columnconfigure(1, weight=1)
    route_grid.grid_columnconfigure(3, weight=1)

    ttk.Label(route_grid, text="Nereden", style="Section.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 4))
    ttk.Combobox(route_grid, values=Sehirler.sehir_listesi, textvariable=nereden_var).grid(
        row=1, column=0, columnspan=2, sticky="ew", padx=(0, 10)
    )
    ttk.Label(route_grid, text="Nereye", style="Section.TLabel").grid(row=0, column=2, sticky="w", pady=(0, 4))
    ttk.Combobox(route_grid, values=Sehirler.sehir_listesi, textvariable=nereye_var).grid(
        row=1, column=2, columnspan=2, sticky="ew"
    )
    ttk.Label(route_grid, text="Tarih", style="Section.TLabel").grid(row=2, column=0, sticky="w", pady=(14, 4))
    DateEntry(route_grid, textvariable=tarih_var, date_pattern="dd.MM.yyyy", width=16).grid(
        row=3, column=0, sticky="w"
    )
    ttk.Button(
        route_grid,
        text="Bugün",
        style="Ghost.TButton",
        command=lambda: tarih_var.set(current_date),
    ).grid(row=3, column=1, sticky="w")
    ttk.Label(route_grid, text="Saat", style="Section.TLabel").grid(row=2, column=2, sticky="w", pady=(14, 4))
    ttk.Entry(route_grid, textvariable=saat_var, width=18).grid(row=3, column=2, sticky="ew", padx=(0, 10))
    ttk.Label(route_grid, text="Örnek 12:30", style="CardText.TLabel").grid(row=3, column=3, sticky="w")

    preferences_frame = ttk.LabelFrame(content_frame, text="Arama Tercihleri", style="Card.TLabelframe")
    preferences_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
    ttk.Label(preferences_frame, text="Bilet tipi seçimi", style="Section.TLabel").pack(anchor="w")

    seat_type_row = ttk.Frame(preferences_frame, style="CardInner.TFrame")
    seat_type_row.pack(fill=tk.X, pady=(6, 10))
    ttk.Checkbutton(seat_type_row, text="Ekonomi", variable=ekonomi_var).pack(side=tk.LEFT, padx=(0, 18))
    ttk.Checkbutton(seat_type_row, text="Business", variable=business_var).pack(side=tk.LEFT)

    ttk.Label(preferences_frame, text="Yeniden deneme aralığı", style="Section.TLabel").pack(anchor="w")
    ttk.Scale(preferences_frame, from_=1, to=30, orient=tk.HORIZONTAL, variable=delay_time_var).pack(fill=tk.X, pady=(6, 2))
    delay_time_label = ttk.Label(preferences_frame, text="1 dakika", style="CardText.TLabel")
    delay_time_label.pack(anchor="w")

    notification_frame = ttk.LabelFrame(content_frame, text="Bildirimler", style="Card.TLabelframe")
    notification_frame.grid(row=0, column=1, sticky="nsew", pady=(0, 10))
    ttk.Checkbutton(
        notification_frame,
        text="Bilet bulununca Telegram bildirimi gönder",
        variable=telegram_msg_var,
    ).pack(anchor="w", pady=(0, 8))
    ttk.Label(notification_frame, text="Bot Token", style="Section.TLabel").pack(anchor="w")
    bot_token_entry = ttk.Entry(notification_frame, textvariable=bot_token_var)
    bot_token_entry.pack(fill=tk.X, pady=(4, 8))
    ttk.Label(notification_frame, text="Chat ID", style="Section.TLabel").pack(anchor="w")
    chat_id_entry = ttk.Entry(notification_frame, textvariable=chat_id_var)
    chat_id_entry.pack(fill=tk.X, pady=(4, 8))
    ttk.Checkbutton(
        notification_frame,
        text="Bilet bulununca sesli bildirim çal",
        variable=ses_var,
    ).pack(anchor="w", pady=(4, 0))

    controls_frame = ttk.LabelFrame(content_frame, text="Kontrol Paneli", style="Card.TLabelframe")
    controls_frame.grid(row=1, column=1, sticky="nsew", pady=(0, 10))

    controls_top = ttk.Frame(controls_frame, style="CardInner.TFrame")
    controls_top.pack(fill=tk.X, pady=(0, 10))
    btn_start = ttk.Button(controls_top, text="Aramayı Başlat", style="Primary.TButton")
    btn_start.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
    btn_stop = ttk.Button(controls_top, text="Durdur", style="Danger.TButton", state=tk.DISABLED)
    btn_stop.pack(side=tk.LEFT)

    controls_links = ttk.Frame(controls_frame, style="CardInner.TFrame")
    controls_links.pack(fill=tk.X, pady=(0, 10))

    controls_help = ttk.Frame(controls_frame, style="CardInner.TFrame")
    controls_help.pack(fill=tk.X)
    ttk.Button(
        controls_help,
        text="GitHub Sayfası",
        style="Ghost.TButton",
        command=lambda: wbopen("https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol"),
    ).pack(side=tk.LEFT, padx=(0, 8))
    btn_toggle = ttk.Button(controls_help, text="Logu Gizle", style="Ghost.TButton")
    btn_toggle.pack(side=tk.LEFT, padx=(0, 8))
    ttk.Button(
        controls_help,
        text="Destek Ol",
        style="Ghost.TButton",
        command=lambda: wbopen("https://www.buymeacoffee.com/mcagriaksoy"),
    ).pack(side=tk.LEFT)

    status_frame = ttk.LabelFrame(content_frame, text="Çalışma Durumu", style="Card.TLabelframe")
    status_frame.grid(row=2, column=1, sticky="nsew")
    ttk.Label(status_frame, text="Canlı durum", style="Section.TLabel").pack(anchor="w")
    ttk.Label(
        status_frame,
        textvariable=run_status_var,
        style="CardText.TLabel",
        font=("Segoe UI Semibold", 12),
    ).pack(anchor="w", pady=(4, 10))
    loader = ttk.Progressbar(status_frame, mode="indeterminate", style="Status.Horizontal.TProgressbar")
    loader.pack(fill=tk.X, pady=(0, 10))
    ttk.Label(
        status_frame,
        text="Uygulama her turda sayfayı açıp seferi kontrol eder. Durdur dediğinizde bekleme döngüsü kesilir.",
        style="CardText.TLabel",
        wraplength=250,
        justify="left",
    ).pack(anchor="w")

    footer_frame = ttk.Frame(main_frame, style="App.TFrame")
    footer_frame.pack(fill=tk.X, pady=(8, 0))
    ttk.Label(
        footer_frame,
        text="Mehmet C. Aksoy tarafından geliştirilen fork sürümü. Açık kaynak topluluğuna teşekkürler.",
        style="Muted.TLabel",
    ).pack(side=tk.LEFT)

    log_container = ttk.LabelFrame(content_frame, text="Arama Logları", style="Card.TLabelframe")
    log_container.grid(row=2, column=0, sticky="nsew")
    log_text = ScrolledText(
        log_container,
        height=14,
        state=tk.NORMAL,
        bg="#0f1720",
        fg="#d8e2ee",
        insertbackground="#d8e2ee",
        relief="flat",
        font=("Cascadia Mono", 9),
        wrap="word",
    )
    log_text.pack(fill=tk.BOTH, expand=True)

    def append_log(message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        def _append():
            log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            log_text.see(tk.END)

        root.after(0, _append)

    def set_run_status(message):
        root.after(0, lambda: run_status_var.set(message))

    def set_running(is_running):
        def _set():
            if is_running:
                btn_start.config(state=tk.DISABLED)
                btn_stop.config(state=tk.NORMAL)
                loader.start(12)
            else:
                btn_start.config(state=tk.NORMAL)
                btn_stop.config(state=tk.DISABLED)
                loader.stop()

        root.after(0, _set)

    def update_delay_label(*_args):
        value = int(delay_time_var.get())
        delay_time_label.config(text=f"{value} dakika")

    delay_time_var.trace_add("write", update_delay_label)
    update_delay_label()

    def toggle_telegram_inputs(*_args):
        state = tk.NORMAL if telegram_msg_var.get() else tk.DISABLED
        bot_token_entry.config(state=state)
        chat_id_entry.config(state=state)

    telegram_msg_var.trace_add("write", toggle_telegram_inputs)
    toggle_telegram_inputs()

    log_visible = {"value": True}

    def on_toggle():
        log_visible["value"] = not log_visible["value"]
        if log_visible["value"]:
            log_container.grid()
            btn_toggle.config(text="Logu Gizle")
            center_geometry(root, *APP_SIZE)
        else:
            log_container.grid_remove()
            btn_toggle.config(text="Logu Göster")
            center_geometry(root, *COMPACT_SIZE)

    btn_toggle.config(command=on_toggle)

    def check_updates(show_message=False):
        update_status_var.set("Sürüm kontrol ediliyor...")
        update_detail_var.set(f"Yüklü sürüm: v{current_version}")

        def worker():
            try:
                release = fetch_latest_release_info()
                latest_release_url["value"] = release["html_url"]
                latest_version = release["version"] or release["tag_name"]
                published_text = (
                    release["published_at"][:10]
                    if release["published_at"]
                    else "Tarih bilinmiyor"
                )
                if parse_version_tuple(latest_version) > parse_version_tuple(current_version):
                    status = f"Yeni sürüm mevcut: v{latest_version}"
                    detail = f"Yüklü sürüm v{current_version}. Yayın tarihi: {published_text}"
                else:
                    status = f"En güncel sürüm sizde: v{current_version}"
                    detail = f"GitHub son sürümü: {release['tag_name']} | {published_text}"

                root.after(0, lambda: update_status_var.set(status))
                root.after(0, lambda: update_detail_var.set(detail))
                if show_message:
                    root.after(
                        0,
                        lambda: messagebox.showinfo("Sürüm Kontrolü", f"{status}\n{detail}"),
                    )
            except (HTTPError, URLError, TimeoutError, ValueError) as exc:
                root.after(0, lambda: update_status_var.set("Sürüm kontrolü yapılamadı"))
                root.after(0, lambda: update_detail_var.set(f"Bağlantı hatası: {exc}"))
                if show_message:
                    root.after(
                        0,
                        lambda: messagebox.showwarning(
                            "Sürüm Kontrolü",
                            "GitHub releases bilgisi şu anda alınamadı.",
                        ),
                    )

        Thread(target=worker, daemon=True).start()

    ttk.Button(
        status_actions,
        text="Sürüm Kontrol Et",
        style="Ghost.TButton",
        command=lambda: check_updates(show_message=True),
    ).pack(side=tk.LEFT, padx=(0, 8))
    ttk.Button(
        status_actions,
        text="Sürüm Notlarını Gör",
        style="Primary.TButton",
        command=lambda: wbopen(latest_release_url["value"]),
    ).pack(side=tk.LEFT)

    def on_start():
        try:
            payload = validate_form()
        except ValueError as exc:
            messagebox.showwarning("Form Hatası", str(exc))
            return

        append_log(
            f"Arama başladı: {payload['nereden']} -> {payload['nereye']} | {payload['tarih']} {payload['saat']}"
        )
        set_run_status("Arama aktif")
        set_running(True)

        def thread_runner():
            global g_isStopped
            g_isStopped = False
            attempt = 0

            while not g_isStopped:
                attempt += 1
                set_run_status(f"Deneme {attempt} çalışıyor")
                append_log(f"Deneme #{attempt} başlatıldı.")

                driver = driver_setting()
                if driver is None:
                    append_log("Tarayıcı başlatılamadı. Edge ve sürücü kurulumunu kontrol edin.")
                    set_run_status("Tarayıcı başlatılamadı")
                    break

                try:
                    append_log("TCDD sayfası yükleniyor...")
                    driver_get(driver)
                    if g_isStopped:
                        safe_driver_quit(driver)
                        break

                    append_log("Rota bilgileri giriliyor...")
                    route_ok = route(
                        driver,
                        payload["nereden"],
                        payload["nereye"],
                        payload["tarih"],
                    )
                    if not route_ok:
                        append_log("Rota bilgileri girilemedi veya işlem durduruldu.")
                        continue

                    append_log("Sefer uygunluk kontrolü yapılıyor...")
                    result = control(
                        driver,
                        payload["saat"],
                        payload["delay_time"],
                        payload["telegram_msg"],
                        payload["bot_token"],
                        payload["chat_id"],
                        payload["ses"],
                        payload["allow_economy"],
                        payload["allow_business"],
                    )
                    if result == ErrCodes.BASARILI:
                        set_run_status("Bilet bulundu")
                        break
                    if result == ErrCodes.GUZERGAH_HATASI:
                        set_run_status("Güzergah hatası")
                        break
                except InvalidSessionIdException as exc:
                    append_log(f"Tarayıcı oturumu beklenmedik şekilde kapandı: {exc}")
                    set_run_status("Tarayıcı oturumu kapandı")
                    safe_driver_quit(driver)
                    break
                except Exception as exc:
                    append_log(f"Beklenmeyen hata: {exc}")
                    set_run_status("Beklenmeyen hata")
                    safe_driver_quit(driver)
                    break

                append_log(f"{payload['delay_time']} dakika bekleniyor.")
                set_run_status("Bekleme modunda")
                for _ in range(payload["delay_time"] * 60):
                    if g_isStopped:
                        append_log("Bekleme döngüsü kullanıcı tarafından durduruldu.")
                        break
                    sleep(1)

            if g_isStopped:
                set_run_status("Kullanıcı tarafından durduruldu")
            set_running(False)

        Thread(target=thread_runner, daemon=True).start()

    def on_stop():
        global g_isStopped
        g_isStopped = True
        append_log("Durdur komutu alındı.")
        set_run_status("Durduruluyor")
        set_running(False)

    btn_start.config(command=on_start)
    btn_stop.config(command=on_stop)

    def show_welcome():
        temp_file = os.path.join(os.getenv("TEMP", os.getcwd()), "tcdd_bilet_cfg.txt")
        if os.path.exists(temp_file):
            return
        messagebox.showinfo(
            "Hoş Geldiniz",
            "İlk tarama biraz zaman alabilir. Sürüm kontrolü ve log paneli artık ana ekranda görünebilir.",
        )
        try:
            with open(temp_file, "w", encoding="utf-8") as file:
                file.write("1")
        except OSError:
            pass

    root.after(120, show_welcome)
    root.after(300, check_updates)
    root.mainloop()


def __main__():
    main()
