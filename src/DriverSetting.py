"""
@author: Mehmet Çağrı Aksoy
"""

from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

class DriverSetting:
    """Driver'ı ayarlar."""
    def __init__(self):
        self.driver = None

    def driver_init(self):
        try:
            options = EdgeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option("detach", True)
            self.driver = Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
            return self.driver
        except Exception as e:
            print(f"Driver ayarlarında hata oluştu: {e}")
            return None
    
    def driver_quit(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

