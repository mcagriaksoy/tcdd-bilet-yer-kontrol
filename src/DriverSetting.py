"""
@author: Mehmet Çağrı Aksoy
"""

from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class DriverSetting:
    """Driver'ı ayarlar."""

    def driver_init(self):
        driver = Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        return driver
