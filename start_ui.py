"""TCDD Bilet Yer Kontrol - tek giris noktasi.

Uygulamayi baslatir, yerel web arayuzunu ayaga kaldirir ve native bir masaustu
penceresinde gosterir. Kullaniciya tarayici penceresi acilmaz.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import threading
import webbrowser
from pathlib import Path
from time import sleep
from urllib.error import URLError
from urllib.request import urlopen

PROJECT_ROOT = Path(__file__).resolve().parent
APP_HOME = (
    Path(sys.executable).resolve().parent
    if getattr(sys, "frozen", False)
    else PROJECT_ROOT
)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5001
PORT_SEARCH_RANGE = 20
READY_TIMEOUT_SECONDS = 30
WINDOW_TITLE = "TCDD Bilet Yer Kontrol"
WINDOW_SIZE = (1180, 820)
WINDOW_MIN_SIZE = (900, 600)

logger = logging.getLogger(__name__)


def _force_utf8_stdio() -> None:
    """Konsolu olmayan (windowed EXE) calisma modunda da print/write guvenli olsun."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            try:
                setattr(sys, stream_name, open(os.devnull, "w", encoding="utf-8"))
            except OSError:
                pass
            continue
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _show_fatal_error(message: str) -> None:
    """Konsolu olmayan EXE build'lerinde de hatayi kullaniciya goster."""
    if os.name == "nt":
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(0, message, WINDOW_TITLE, 0x10)
            return
        except Exception:
            pass
    print(message, file=sys.stderr)


def _prepare_runtime() -> None:
    """Calisma dizinini ve log klasorunu hazirla."""
    if APP_HOME.exists():
        os.chdir(APP_HOME)

    logs_dir = APP_HOME / "logs"
    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            handlers=[
                logging.FileHandler(logs_dir / "app.log", encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
    except OSError:
        logging.basicConfig(level=logging.INFO)


def _default_port() -> int:
    raw_port = os.environ.get("TCDD_WEB_PORT", str(DEFAULT_PORT))
    try:
        return int(raw_port)
    except ValueError:
        return DEFAULT_PORT


def _create_server(app, host: str, port: int, exact_port: bool):
    from werkzeug.serving import make_server

    candidates = [port] if exact_port else range(port, port + PORT_SEARCH_RANGE)
    last_error = None
    for candidate in candidates:
        try:
            return make_server(host, candidate, app, threaded=True)
        except OSError as exc:
            last_error = exc
            logger.warning("Port %s kullanilamiyor: %s", candidate, exc)
    raise OSError(
        f"{port}-{port + PORT_SEARCH_RANGE - 1} araliginda bos port bulunamadi."
    ) from last_error


class ServerThread(threading.Thread):
    """Flask/Werkzeug sunucusunu arka planda calistirir."""

    def __init__(self, server):
        super().__init__(name="web-server", daemon=True)
        self._server = server

    def run(self) -> None:
        try:
            self._server.serve_forever()
        except Exception:
            logger.exception("Web sunucusu beklenmedik sekilde durdu.")

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()


def _wait_until_ready(url: str) -> bool:
    status_url = f"{url}/api/status"
    deadline = READY_TIMEOUT_SECONDS * 4
    for _ in range(deadline):
        try:
            with urlopen(status_url, timeout=1):
                return True
        except (URLError, OSError):
            sleep(0.25)
    return False


def _start_driver_download() -> None:
    """Ilk acilista WebDriver'i arka planda indirmeye calis."""
    try:
        from backend.driver_setting import ensure_driver_downloaded, has_local_driver
    except Exception as exc:  # pragma: no cover - beklenmeyen kurulum hatasi
        logger.warning("WebDriver modulu yuklenemedi: %s", exc)
        return

    if has_local_driver():
        return

    def worker() -> None:
        logger.info("WebDriver bulunamadi, indirme baslatiliyor...")
        try:
            path = ensure_driver_downloaded()
        except Exception as exc:
            logger.warning("WebDriver indirilemedi: %s", exc)
            return
        if path:
            logger.info("WebDriver hazir: %s", path)
        else:
            logger.warning("WebDriver indirilemedi.")

    threading.Thread(target=worker, name="driver-download", daemon=True).start()


def _choose_window_geometry(webview):
    """Pencereyi ekrana sigacak sekilde boyutlandir."""
    try:
        screen = webview.screens[0]
        available_width = int(screen.width * 0.92)
        available_height = int(screen.height * 0.9)
    except Exception:
        return WINDOW_SIZE, WINDOW_MIN_SIZE

    width = max(WINDOW_MIN_SIZE[0], min(WINDOW_SIZE[0], available_width))
    height = max(WINDOW_MIN_SIZE[1], min(WINDOW_SIZE[1], available_height))
    return (width, height), (min(WINDOW_MIN_SIZE[0], width), min(WINDOW_MIN_SIZE[1], height))


def _open_native_window(url: str) -> int:
    if sys.platform.startswith("linux"):
        # pywebview once GTK'yi deneyip konsola hata basiyor; Qt backend'ini
        # bastan secerek bu gurultuyu engelliyoruz.
        os.environ.setdefault("PYWEBVIEW_GUI", "qt")

    try:
        import webview
    except Exception as exc:
        message = (
            "Masaustu penceresi icin pywebview gerekli.\n\n"
            "Kurulum: pip install pywebview\n"
            f"\nAyrinti: {exc}"
        )
        logger.exception("pywebview yuklenemedi")
        _show_fatal_error(message)
        return 1

    size, min_size = _choose_window_geometry(webview)
    webview.create_window(
        WINDOW_TITLE,
        url,
        width=size[0],
        height=size[1],
        min_size=min_size,
        text_select=True,
        background_color="#f4f7fb",
    )

    start_options = {}
    if sys.platform.startswith("linux"):
        # GTK kurulu olmadiginda pywebview once GTK'yi deneyip konsola hata
        # basiyor; Qt backend'i acikca secerek bu gurultuyu engelliyoruz.
        start_options["gui"] = "qt"

    icon_path = APP_HOME / "icon.ico"
    if os.name == "nt" and icon_path.exists():
        start_options["icon"] = str(icon_path)

    try:
        webview.start(**start_options)
    except Exception as exc:
        message = (
            "Masaustu penceresi acilamadi.\n\n"
            "Windows'ta WebView2 calisma zamaninin kurulu oldugundan emin olun.\n"
            "Linux'ta Qt bagimliliklarini kurun: pip install \"pywebview[qt]\"\n"
            f"\nAyrinti: {exc}"
        )
        logger.exception("Native pencere baslatilamadi")
        _show_fatal_error(message)
        return 1
    return 0


def _parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TCDD Bilet Yer Kontrol arayuzunu baslatir."
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("TCDD_WEB_HOST", DEFAULT_HOST),
        help=f"Sunucu adresi (varsayilan: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help=f"Sunucu portu (varsayilan: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        help="Native pencere yerine varsayilan tarayiciyi kullan (gelistirici secenegi).",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    _force_utf8_stdio()
    args = _parse_args(argv)
    _prepare_runtime()

    if args.host not in (DEFAULT_HOST, "localhost"):
        os.environ.setdefault("TCDD_ALLOW_REMOTE", "1")

    os.environ.setdefault("TCDD_WEB_HOST", args.host)

    try:
        from webapp import create_app
    except Exception as exc:
        message = f"Uygulama baslatilamadi: {exc}"
        logger.exception(message)
        _show_fatal_error(message)
        return 1

    port = args.port if args.port is not None else _default_port()
    app = create_app()

    try:
        server = _create_server(app, args.host, port, exact_port=args.port is not None)
    except OSError as exc:
        message = f"Sunucu baslatilamadi: {exc}"
        logger.exception(message)
        _show_fatal_error(message)
        return 1

    actual_port = server.server_port
    local_host = "127.0.0.1" if args.host in ("0.0.0.0", "::") else args.host
    url = f"http://{local_host}:{actual_port}"
    logger.info("Arayuz hazir: %s (dinlenen adres: %s)", url, args.host)

    server_thread = ServerThread(server)
    server_thread.start()

    if not _wait_until_ready(url):
        server_thread.stop()
        message = "Arayuz zamaninda baslatilamadi. Loglari kontrol edin."
        logger.error(message)
        _show_fatal_error(message)
        return 1

    _start_driver_download()

    try:
        if args.browser:
            webbrowser.open(url, new=2)
            print(f"Arayuz tarayicida acildi: {url}  (kapatmak icin Ctrl+C)")
            try:
                server_thread.join()
            except KeyboardInterrupt:
                print("\nKapatiliyor...")
            return 0
        return _open_native_window(url)
    finally:
        server_thread.stop()
        server_thread.join(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
