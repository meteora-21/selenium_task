from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriverSingleton:
    _instance = None

    def __new__(cls, config, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.config = config
            cls._instance.driver = cls._instance._initialize_driver()
        return cls._instance

    def _initialize_driver(self):
        chrome_options = Options()
        options = self.config.get("options")
        for option in options:
            chrome_options.add_argument(option)

        return webdriver.Chrome(options=chrome_options)

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
        WebDriverSingleton._instance = None
