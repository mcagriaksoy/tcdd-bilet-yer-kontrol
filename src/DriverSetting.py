"""
@author: Mehmet Çağrı Aksoy
"""

from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

class DriverSetting:
    """Driver'ı ayarlar."""

    def driver_init(self):
        options = EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        return driver
