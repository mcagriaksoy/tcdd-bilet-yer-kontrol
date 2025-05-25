"""
@author: Mehmet Çağrı Aksoy
"""

import tempfile
from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class DriverSetting:
    """Driver'ı ayarlar."""
    def __init__(self):
        self.driver = None

    def driver_init(self):
        try:
            options = EdgeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option("detach", True)
            '''
            options.add_experimental_option("prefs", { 
                "profile.default_content_setting_values.notifications": 2,  # Disable notifications
                "profile.default_content_setting_values.popups": 0,  # Disable popups
                "profile.default_content_setting_values.geolocation": 2,  # Disable geolocation
                "profile.default_content_setting_values.media_stream": 2,  # Disable media stream
                "profile.default_content_setting_values.midi_sysex": 2,  # Disable MIDI
                "profile.default_content_setting_values.protected_media_identifier": 2,  # Disable protected media
                })
            '''
            # Create a temporary directory for user data
            temp_user_data_dir = tempfile.mkdtemp()
            options.add_argument(f"--user-data-dir={temp_user_data_dir}")
            options.add_argument('--disable-blink-features=AutomationControlled')
            '''
            options.add_argument('--start-minimized')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            '''
            self.driver = Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
            return self.driver
        except Exception as e:
            print(f"Driver ayarlarında hata oluştu: {e}")
            return None
    
    def driver_quit(self):
        if self.driver:
            self.driver.quit()
            self.driver = None