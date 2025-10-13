"""
@author: Mehmet Çağrı Aksoy
"""

import tempfile
import os
import shutil
from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging
import ctypes


class DriverSetting:
    """Driver'ı ayarlar."""

    def __init__(self):
        self.driver = None
        self.temp_user_data_dir = None
        # Configure logging only once
        if not logging.getLogger().handlers:
            logging.basicConfig(
                filename=os.path.join(os.getcwd(), "tcdd_debug.log"),
                level=logging.DEBUG,
                format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            )
        self.logger = logging.getLogger(__name__)

    def _notify_user(self, message, title="TCDD Bilet"):
        try:
            # Windows MessageBox (unicode)
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
        except Exception as e:
            self.logger.debug(f"Popup failed: {e}")

    def driver_init(self):
        try:
            options = EdgeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_experimental_option("detach", True)
            """
            options.add_experimental_option("prefs", { 
                "profile.default_content_setting_values.notifications": 2,  # Disable notifications
                "profile.default_content_setting_values.popups": 0,  # Disable popups
                "profile.default_content_setting_values.geolocation": 2,  # Disable geolocation
                "profile.default_content_setting_values.media_stream": 2,  # Disable media stream
                "profile.default_content_setting_values.midi_sysex": 2,  # Disable MIDI
                "profile.default_content_setting_values.protected_media_identifier": 2,  # Disable protected media
                })
            """
            # Create a temporary directory for user data
            temp_user_data_dir = tempfile.mkdtemp()
            self.temp_user_data_dir = temp_user_data_dir
            options.add_argument(f"--user-data-dir={temp_user_data_dir}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            """
            options.add_argument('--start-minimized')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            """
            # Primary attempt: use webdriver_manager to install driver
            try:
                driver_path = EdgeChromiumDriverManager().install()
                service = EdgeService(driver_path)
                self.driver = Edge(service=service, options=options)
                self.logger.info("Edge driver started with WebDriverManager.")
                return self.driver
            except Exception as wm_err:
                self.logger.warning(f"WebDriverManager hatası: {wm_err}. Yerel sürücü veya PATH üzerinden başlatma deneniyor.")

                # 1) Check env vars and PATH
                driver_path = os.environ.get("EDGE_DRIVER_PATH") or os.environ.get("EDGEWEBDRIVER") or shutil.which("msedgedriver")

                # 2) Common locations to check (Windows typical locations)
                common_paths = [
                    os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "Microsoft", "Edge", "Application", "msedgedriver.exe"),
                    os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"), "Microsoft", "Edge", "Application", "msedgedriver.exe"),
                    os.path.join(os.getcwd(), "msedgedriver.exe"),
                ]
                for p in common_paths:
                    if p and os.path.exists(p):
                        driver_path = p
                        break

                # 3) If we found a driver path, try to start with it
                if driver_path:
                    try:
                        service = EdgeService(driver_path)
                        self.driver = Edge(service=service, options=options)
                        self.logger.info(f"Edge driver started using local driver at {driver_path}.")
                        return self.driver
                    except Exception as local_err:
                        self.logger.exception(f"Yerel sürücü ile başlatma başarısız ({driver_path}): {local_err}")

                # 4) Final fallback: try to start Edge without explicit service (selenium may locate driver automatically)
                try:
                    self.driver = Edge(options=options)
                    self.logger.info("Edge started without explicit service.")
                    return self.driver
                except Exception as final_err:
                    self.logger.exception(f"Edge sürücüsüz başlatılamadı: {final_err}")
                    # Inform user with popup
                    self._notify_user("Edge sürücüsü başlatılamadı. Lütfen sürücüyü kontrol edin ve tekrar deneyin.", "Driver Başlatma Hatası")
                    return None

        except Exception as e:
            self.logger.exception(f"Driver ayarlarında hata oluştu: {e}")
            self._notify_user(f"Driver ayarlarında hata oluştu: {e}", "Driver Hatası")
            return None

    def driver_quit(self):
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Driver quit successfully.")
            except Exception as e:
                self.logger.exception(f"Driver quit sırasında hata: {e}")
            finally:
                self.driver = None

        # Clean up temp user data dir
        if self.temp_user_data_dir:
            try:
                shutil.rmtree(self.temp_user_data_dir, ignore_errors=True)
                self.logger.debug(f"Temporary user data dir removed: {self.temp_user_data_dir}")
            except Exception as e:
                self.logger.exception(f"Temp dir cleanup failed: {e}")
            finally:
                self.temp_user_data_dir = None
