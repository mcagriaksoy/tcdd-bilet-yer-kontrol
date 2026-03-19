"""
@author: Mehmet Çağrı Aksoy
"""

import ctypes
import logging
import os
import platform
import shutil
import subprocess
import tempfile
import zipfile
from io import BytesIO
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class DriverSetting:
    """Driver'ı ayarlar."""

    def __init__(self):
        self.driver = None
        self.temp_user_data_dir = None
        if not logging.getLogger().handlers:
            logging.basicConfig(
                filename=os.path.join(os.getcwd(), "tcdd_debug.log"),
                level=logging.DEBUG,
                format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            )
        self.logger = logging.getLogger(__name__)

    def _notify_user(self, message, title="TCDD Bilet"):
        try:
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
        except Exception as exc:
            self.logger.debug(f"Popup failed: {exc}")

    def _build_options(self):
        options = EdgeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.temp_user_data_dir = tempfile.mkdtemp(prefix="tcdd-edge-")
        options.add_argument(f"--user-data-dir={self.temp_user_data_dir}")

        edge_binary = self._find_edge_binary()
        if edge_binary:
            options.binary_location = edge_binary
            self.logger.info(f"Edge binary bulundu: {edge_binary}")

        return options

    def _find_edge_binary(self):
        candidates = [
            os.environ.get("EDGE_BINARY_PATH"),
            os.path.join(
                os.environ.get("PROGRAMFILES", "C:\\Program Files"),
                "Microsoft",
                "Edge",
                "Application",
                "msedge.exe",
            ),
            os.path.join(
                os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"),
                "Microsoft",
                "Edge",
                "Application",
                "msedge.exe",
            ),
        ]
        for path in candidates:
            if path and os.path.exists(path):
                return path
        return None

    def _get_edge_version(self):
        edge_binary = self._find_edge_binary()
        if not edge_binary:
            return None
        try:
            command = [
                "powershell",
                "-NoProfile",
                "-Command",
                f"(Get-Item '{edge_binary}').VersionInfo.ProductVersion",
            ]
            version = subprocess.check_output(command, text=True).strip()
            return version or None
        except Exception as exc:
            self.logger.debug(f"Edge sürümü okunamadı: {exc}")
            return None

    def _driver_asset_name(self):
        machine = platform.machine().lower()
        if "64" in machine or machine == "amd64":
            return "edgedriver_win64.zip"
        return "edgedriver_win32.zip"

    def _get_driver_version(self, driver_path):
        if not driver_path or not os.path.exists(driver_path):
            return None
        try:
            command = [driver_path, "--version"]
            output = subprocess.check_output(command, text=True).strip()
            parts = output.split()
            if len(parts) >= 2:
                return parts[1]
        except Exception as exc:
            self.logger.debug(f"Driver sürümü okunamadı ({driver_path}): {exc}")
        return None

    def _is_driver_compatible(self, driver_path, edge_version):
        if not driver_path or not edge_version:
            return False
        driver_version = self._get_driver_version(driver_path)
        if not driver_version:
            return False
        edge_major = edge_version.split(".")[0]
        driver_major = driver_version.split(".")[0]
        compatible = edge_major == driver_major
        self.logger.info(
            f"Driver uyumluluk kontrolü: edge={edge_version}, driver={driver_version}, compatible={compatible}"
        )
        return compatible

    def _find_local_driver(self):
        candidates = [
            os.environ.get("EDGE_DRIVER_PATH"),
            os.environ.get("EDGEWEBDRIVER"),
            shutil.which("msedgedriver"),
            os.path.join(os.getcwd(), "msedgedriver.exe"),
        ]
        for path in candidates:
            if path and os.path.exists(path):
                return path
        return None

    def _cleanup_temp_dir(self):
        if self.temp_user_data_dir:
            try:
                shutil.rmtree(self.temp_user_data_dir, ignore_errors=True)
            except Exception as exc:
                self.logger.debug(f"Temp dir cleanup failed: {exc}")
            finally:
                self.temp_user_data_dir = None

    def _start_with_service(self, options, driver_path):
        service = EdgeService(driver_path)
        self.driver = Edge(service=service, options=options)
        self.logger.info(f"Edge driver başlatıldı: {driver_path}")
        return self.driver

    def _download_driver_from_url(self, url, destination_path):
        request = Request(url, headers={"User-Agent": "tcdd-bilet-yer-kontrol"})
        with urlopen(request, timeout=20) as response:
            archive_data = response.read()

        with zipfile.ZipFile(BytesIO(archive_data)) as archive:
            for member in archive.namelist():
                if member.lower().endswith("msedgedriver.exe"):
                    with archive.open(member) as source, open(
                        destination_path, "wb"
                    ) as target:
                        shutil.copyfileobj(source, target)
                    return destination_path
        raise FileNotFoundError("İndirilen pakette msedgedriver.exe bulunamadı.")

    def _auto_download_driver(self):
        edge_version = self._get_edge_version()
        if not edge_version:
            self.logger.warning("Edge sürümü okunamadığı için otomatik indirme atlandı.")
            return None

        version_candidates = [edge_version]
        parts = edge_version.split(".")
        if len(parts) >= 3:
            version_candidates.append(".".join(parts[:3]))

        asset_name = self._driver_asset_name()
        destination_path = os.path.join(os.getcwd(), "msedgedriver.exe")

        for version in version_candidates:
            urls = [
                f"https://msedgedriver.microsoft.com/{version}/{asset_name}",
                f"https://msedgedriver.azureedge.net/{version}/{asset_name}",
                f"https://msedgewebdriverstorage.z22.web.core.windows.net/{version}/{asset_name}",
            ]
            for url in urls:
                try:
                    self.logger.info(f"Edge driver indirilmeye çalışılıyor: {url}")
                    downloaded_path = self._download_driver_from_url(url, destination_path)
                    self.logger.info(f"Edge driver indirildi: {downloaded_path}")
                    return downloaded_path
                except (HTTPError, URLError, TimeoutError, zipfile.BadZipFile, FileNotFoundError) as exc:
                    self.logger.warning(f"Edge driver indirilemedi ({url}): {exc}")
                except Exception as exc:
                    self.logger.warning(f"Beklenmeyen indirme hatası ({url}): {exc}")
        return None

    def _ensure_local_driver(self):
        edge_version = self._get_edge_version()
        local_driver = self._find_local_driver()

        if local_driver and self._is_driver_compatible(local_driver, edge_version):
            self.logger.info(f"Uyumlu yerel driver kullanılacak: {local_driver}")
            return local_driver

        if local_driver and os.path.abspath(local_driver) == os.path.join(
            os.getcwd(), "msedgedriver.exe"
        ):
            try:
                os.remove(local_driver)
                self.logger.info(f"Eski veya uyumsuz driver silindi: {local_driver}")
            except OSError as exc:
                self.logger.warning(f"Eski driver silinemedi ({local_driver}): {exc}")

        downloaded_driver = self._auto_download_driver()
        if downloaded_driver and self._is_driver_compatible(downloaded_driver, edge_version):
            return downloaded_driver

        return local_driver

    def driver_init(self):
        try:
            options = self._build_options()

            local_driver = self._ensure_local_driver()
            if local_driver:
                try:
                    return self._start_with_service(options, local_driver)
                except Exception as local_err:
                    self.logger.warning(
                        f"Yerel msedgedriver ile başlatma başarısız ({local_driver}): {local_err}"
                    )

            try:
                self.driver = Edge(options=options)
                self.logger.info("Edge, Selenium Manager ile başlatıldı.")
                return self.driver
            except Exception as selenium_manager_err:
                self.logger.warning(
                    f"Selenium Manager ile başlatma başarısız: {selenium_manager_err}"
                )

            try:
                downloaded_driver = EdgeChromiumDriverManager().install()
                return self._start_with_service(options, downloaded_driver)
            except Exception as wm_err:
                self.logger.warning(
                    f"WebDriverManager ile sürücü indirme/başlatma başarısız: {wm_err}"
                )

            self._notify_user(
                "Edge sürücüsü başlatılamadı.\n\n"
                "Uygulama önce yerel sürücüyü, sonra otomatik indirmeyi denedi.\n"
                "Kontrol etmeniz gerekenler:\n"
                "1. Microsoft Edge yüklü mü?\n"
                "2. Edge güncel mi?\n"
                "3. İnternet veya güvenlik yazılımı sürücü indirmesini engelliyor mu?\n"
                "4. Gerekirse msedgedriver.exe dosyasını uygulama klasörüne koyabilirsiniz.",
                "Driver Başlatma Hatası",
            )
            return None
        except Exception as exc:
            self.logger.exception(f"Driver ayarlarında hata oluştu: {exc}")
            self._notify_user(
                f"Driver ayarlarında hata oluştu:\n{exc}",
                "Driver Hatası",
            )
            self._cleanup_temp_dir()
            return None

    def driver_quit(self):
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Driver quit successfully.")
            except Exception as exc:
                self.logger.exception(f"Driver quit sırasında hata: {exc}")
            finally:
                self.driver = None

        self._cleanup_temp_dir()
