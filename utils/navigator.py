from selenium.webdriver.remote.webdriver import WebDriver
from utils.config_reader import ConfigReader


class Navigator:
    def __init__(self, driver: WebDriver, config: ConfigReader):
        self.driver = driver
        self.config = config
        self.base_url = config.get("base_url")

    def go_to_home_page(self):
        self.driver.get(self.base_url)

    def go_to_login_page(self):
        self.driver.get(f"{self.base_url}{self.config.get('login_page')}")

    def go_to_dashboard(self):
        self.driver.get(f"{self.base_url}{self.config.get('dashboard_page')}")
