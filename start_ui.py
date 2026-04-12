import os
import subprocess
import sys
import tempfile
import tkinter as tk
import webbrowser
from datetime import datetime
from pathlib import Path
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

PROJECT_ROOT = Path(__file__).resolve().parent
APP_HOME = (
    Path(sys.executable).resolve().parent
    if getattr(sys, "frozen", False)
    else PROJECT_ROOT
)
WEB_LOG_PATH = APP_HOME / "web_launcher.log"
DESKTOP_LOG_PATH = APP_HOME / "desktop_launcher.log"


class LauncherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TCDD Bilet Yer Kontrol Başlatıcı")
        self.root.geometry("720x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#f2f6fb")
        self._set_window_icon()

        self.web_process = None
        self.desktop_process = None
        self.web_log = None
        self.desktop_log = None

        self.web_status = tk.StringVar(value="Web Uygulaması: Kapalı")
        self.desktop_status = tk.StringVar(value="Masaüstü Uygulaması: Kapalı")

        self._setup_style()
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.after(1000, self.poll_processes)

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10), background="#f2f6fb", foreground="#17324d")
        style.configure("Shell.TFrame", background="#f2f6fb")
        style.configure(
            "Card.TLabelframe",
            background="#ffffff",
            bordercolor="#d2dfed",
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "Card.TLabelframe.Label",
            background="#ffffff",
            foreground="#17324d",
            font=("Segoe UI Semibold", 10),
        )
        style.configure(
            "Title.TLabel",
            background="#f2f6fb",
            foreground="#123454",
            font=("Segoe UI Semibold", 22),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#f2f6fb",
            foreground="#536a84",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Status.TLabel",
            background="#ffffff",
            foreground="#17324d",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Primary.TButton",
            background="#1467b0",
            foreground="white",
            padding=(12, 8),
            borderwidth=0,
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#0f5b9c"), ("pressed", "#0c4f89")],
        )
        style.configure(
            "Accent.TButton",
            background="#233a59",
            foreground="white",
            padding=(12, 8),
            borderwidth=0,
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#1b304a"), ("pressed", "#16283d")],
        )
        style.configure(
            "Ghost.TButton",
            background="#eaf2fb",
            foreground="#17324d",
            padding=(12, 8),
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.map(
            "Ghost.TButton",
            background=[("active", "#dbeaf9"), ("pressed", "#d1e4f7")],
        )
        style.configure(
            "Danger.TButton",
            background="#b74646",
            foreground="white",
            padding=(12, 8),
            borderwidth=0,
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#a13d3d"), ("pressed", "#8e3535")],
        )

    def _set_window_icon(self):
        icon_candidates = [
            APP_HOME / "icon.ico",
            APP_HOME / "desktop_app" / "icon.ico",
            PROJECT_ROOT / "icon.ico",
            PROJECT_ROOT / "desktop_app" / "icon.ico",
        ]
        for icon_path in icon_candidates:
            if not icon_path.exists():
                continue
            try:
                self.root.iconbitmap(str(icon_path))
                return
            except tk.TclError:
                continue

    def _update_open_web_button_state(self):
        if not hasattr(self, "btn_open_web"):
            return
        state = tk.NORMAL if self._is_running(self.web_process) else tk.DISABLED
        self.btn_open_web.config(state=state)

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=16, style="Shell.TFrame")
        main.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(main, text="TCDD Otomatik Bilet Yer Kontrol Başlatıcısı", style="Title.TLabel")
        title.pack(anchor="w")

        subtitle = ttk.Label(
            main,
            text="Web ve masaüstü uygulamasını tek ekrandan ayrı ayrı veya birlikte başlatın.",
            style="Subtitle.TLabel",
        )
        subtitle.pack(anchor="w", pady=(2, 12))

        status_card = ttk.LabelFrame(main, text="Canlı Durum", padding=12, style="Card.TLabelframe")
        status_card.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(status_card, textvariable=self.web_status, style="Status.TLabel").pack(anchor="w")
        ttk.Label(status_card, textvariable=self.desktop_status, style="Status.TLabel").pack(anchor="w", pady=(6, 0))

        controls = ttk.LabelFrame(main, text="Kontroller", padding=12, style="Card.TLabelframe")
        controls.pack(fill=tk.X, pady=(0, 10))

        row1 = ttk.Frame(controls)
        row1.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(
            row1,
            text="Web Uygulamasını Başlat",
            style="Primary.TButton",
            command=self.start_web,
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            row1,
            text="Masaüstü Uygulamasını Başlat",
            style="Accent.TButton",
            command=self.start_desktop,
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            row1,
            text="İkisini Birlikte Başlat",
            style="Primary.TButton",
            command=self.start_both,
        ).pack(side=tk.LEFT)

        row2 = ttk.Frame(controls)
        row2.pack(fill=tk.X)
        ttk.Button(
            row2,
            text="Web Uygulamasını Durdur",
            style="Ghost.TButton",
            command=self.stop_web,
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            row2,
            text="Masaüstü Uygulamasını Durdur",
            style="Ghost.TButton",
            command=self.stop_desktop,
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            row2,
            text="Tümünü Durdur",
            style="Danger.TButton",
            command=self.stop_all,
        ).pack(side=tk.LEFT, padx=(0, 8))
        self.btn_open_web = ttk.Button(
            row2,
            text="Web Sayfasını Aç",
            style="Ghost.TButton",
            command=self.open_web,
        )
        self.btn_open_web.pack(side=tk.LEFT)
        self._update_open_web_button_state()

        log_box = ttk.LabelFrame(main, text="Başlatıcı Logları", padding=12, style="Card.TLabelframe")
        log_box.pack(fill=tk.BOTH, expand=True)
        self.log_text = ScrolledText(
            log_box,
            height=14,
            font=("Cascadia Mono", 9),
            bg="#0f1720",
            fg="#d7e2ef",
            insertbackground="#d7e2ef",
            relief="flat",
            state=tk.NORMAL,
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self._log("Başlatıcı hazır.")

    def _log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    @staticmethod
    def _is_running(process):
        return process is not None and process.poll() is None

    def _cleanup_stale_web_processes(self):
        if os.name != "nt":
            return
        script = (
            "$procs = Get-CimInstance Win32_Process | "
            "Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match '-m webapp.main' }; "
            "foreach($p in $procs){ "
            "try { Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop; Write-Output $p.ProcessId } "
            "catch {} }"
        )
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", script],
                capture_output=True,
                text=True,
                check=False,
            )
            killed = [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]
            if killed:
                self._log(f"Eski web süreçleri temizlendi: {', '.join(killed)}")
        except Exception as exc:
            self._log(f"Eski web süreçleri temizlenemedi: {exc}")

    def _start_process(self, command, cwd, app_name, log_attr):
        existing = self.web_process if app_name == "web" else self.desktop_process
        if self._is_running(existing):
            app_label = "Web uygulaması" if app_name == "web" else "Masaüstü uygulaması"
            self._log(f"{app_label} zaten çalışıyor.")
            return existing

        log_path = WEB_LOG_PATH if app_name == "web" else DESKTOP_LOG_PATH
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_file = open(log_path, "a", encoding="utf-8")
        except OSError:
            fallback_dir = Path(tempfile.gettempdir()) / "tcdd-launcher-logs"
            fallback_dir.mkdir(parents=True, exist_ok=True)
            log_path = fallback_dir / log_path.name
            log_file = open(log_path, "a", encoding="utf-8")

        kwargs = {
            "cwd": str(cwd),
            "stdout": log_file,
            "stderr": subprocess.STDOUT,
            "text": True,
            "env": {
                **os.environ,
                "PYTHONIOENCODING": "utf-8",
                "PYTHONUTF8": "1",
            },
        }
        if os.name == "nt":
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP

        try:
            process = subprocess.Popen(command, **kwargs)
        except Exception:
            if log_file and not log_file.closed:
                log_file.close()
            raise

        setattr(self, log_attr, log_file)

        if app_name == "web":
            self.web_process = process
            self.web_status.set(f"Web Uygulaması: Çalışıyor (PID {process.pid})")
            self._log(f"Web uygulaması başlatıldı (PID {process.pid}). Log: {log_path.name}")
            self._update_open_web_button_state()
        else:
            self.desktop_process = process
            self.desktop_status.set(f"Masaüstü Uygulaması: Çalışıyor (PID {process.pid})")
            self._log(
                f"Masaüstü uygulaması başlatıldı (PID {process.pid}). Log: {log_path.name}"
            )

        return process

    def _stop_process(self, app_name):
        process = self.web_process if app_name == "web" else self.desktop_process
        log_attr = "web_log" if app_name == "web" else "desktop_log"

        if not self._is_running(process):
            app_label = "Web uygulaması" if app_name == "web" else "Masaüstü uygulaması"
            self._log(f"{app_label} şu an çalışmıyor.")
            if app_name == "web":
                self.web_status.set("Web Uygulaması: Kapalı")
                self.web_process = None
                self._update_open_web_button_state()
            else:
                self.desktop_status.set("Masaüstü Uygulaması: Kapalı")
                self.desktop_process = None
            self._close_log(log_attr)
            return

        process.terminate()
        try:
            process.wait(timeout=6)
            app_label = "Web uygulaması" if app_name == "web" else "Masaüstü uygulaması"
            self._log(f"{app_label} durduruldu.")
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)
            app_label = "Web uygulaması" if app_name == "web" else "Masaüstü uygulaması"
            self._log(f"{app_label} zamanında kapanmadı; zorla kapatıldı.")

        if app_name == "web":
            self.web_process = None
            self.web_status.set("Web Uygulaması: Kapalı")
            self._update_open_web_button_state()
        else:
            self.desktop_process = None
            self.desktop_status.set("Masaüstü Uygulaması: Kapalı")

        self._close_log(log_attr)

    def _close_log(self, log_attr):
        log_file = getattr(self, log_attr)
        if log_file and not log_file.closed:
            log_file.close()
        setattr(self, log_attr, None)

    def start_web(self):
        was_running = self._is_running(self.web_process)
        if not was_running:
            self._cleanup_stale_web_processes()
        if getattr(sys, "frozen", False):
            command = [sys.executable, "--run-web"]
        else:
            command = [sys.executable, "-m", "webapp.main"]
        try:
            self._start_process(
                command,
                APP_HOME,
                "web",
                "web_log",
            )
        except Exception as exc:
            self.web_status.set("Web Uygulaması: Başlatılamadı")
            self._log(f"Web uygulaması başlatılamadı: {exc}")
            self._update_open_web_button_state()
            return
        if not was_running and self._is_running(self.web_process):
            self.open_web()

    def start_desktop(self):
        if getattr(sys, "frozen", False):
            command = [sys.executable, "--run-desktop"]
        else:
            command = [sys.executable, "-m", "desktop_app.main"]
        try:
            self._start_process(
                command,
                APP_HOME,
                "desktop",
                "desktop_log",
            )
        except Exception as exc:
            self.desktop_status.set("Masaüstü Uygulaması: Başlatılamadı")
            self._log(f"Masaüstü uygulaması başlatılamadı: {exc}")
            return

    def start_both(self):
        self.start_web()
        self.start_desktop()

    def stop_web(self):
        self._stop_process("web")
        self._cleanup_stale_web_processes()

    def stop_desktop(self):
        self._stop_process("desktop")

    def stop_all(self):
        self.stop_web()
        self.stop_desktop()

    def open_web(self):
        if not self._is_running(self.web_process):
            self._log("Web uygulaması çalışmadığı için sayfa açılamadı.")
            return
        webbrowser.open("http://127.0.0.1:5000")
        self._log("Web uygulaması tarayıcıda açıldı.")

    def poll_processes(self):
        if self.web_process and self.web_process.poll() is not None:
            code = self.web_process.returncode
            self._log(f"Web uygulaması kapandı (kod {code}).")
            self.web_process = None
            self.web_status.set("Web Uygulaması: Kapalı")
            self._close_log("web_log")
            self._update_open_web_button_state()

        if self.desktop_process and self.desktop_process.poll() is not None:
            code = self.desktop_process.returncode
            self._log(f"Masaüstü uygulaması kapandı (kod {code}).")
            self.desktop_process = None
            self.desktop_status.set("Masaüstü Uygulaması: Kapalı")
            self._close_log("desktop_log")

        self.root.after(1000, self.poll_processes)

    def on_close(self):
        self.stop_all()
        self.root.destroy()


def main():
    if APP_HOME.exists():
        os.chdir(APP_HOME)

    if "--run-web" in sys.argv:
        from webapp.main import main as web_main

        web_main()
        return

    if "--run-desktop" in sys.argv:
        from desktop_app.main import main as desktop_main

        desktop_main()
        return

    app = LauncherApp()
    app.root.mainloop()


if __name__ == "__main__":
    main()




