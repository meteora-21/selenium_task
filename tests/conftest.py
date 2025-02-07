import pytest
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from threading import Lock


class ConfigReader:
    _instance = None
    _lock = Lock()

    def __new__(cls, file_path, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, file_path):
        if not hasattr(self, "_initialized"):
            self.file_path = file_path
            self.config = self._load_config()
            self._initialized = True

    def _load_config(self):
        assert os.path.exists(self.file_path), f"The configuration file {self.file_path} was not found."
        with open(self.file_path, "r") as file:
            return json.load(file)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def update(self, key, value):
        self.config[key] = value
        self.save()

    def save(self):
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.config, file, indent=4)
        except PermissionError:
            raise PermissionError(f'Permission denied while writing to the file: {self.file_path}.')
        except IOError as e:
            raise IOError(f'IO error occurred while saving the configuration file {self.file_path}: {e}')


class WebDriverSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls, config, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config):
        if not hasattr(self, "_initialized"):
            self.config = config
            self.driver = self._initialized_driver()
            self._initialized = True

    def _initialized_driver(self):
        chrome_options = Options()

        options = self.config.get("options", [])

        for option in options:
            chrome_options.add_argument(option)

        return webdriver.Chrome(options=chrome_options)

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        self.driver.quit()
        WebDriverSingleton._instance = None


@pytest.fixture(scope="session")
def config():
    return ConfigReader("../config.json")


@pytest.fixture(scope="function")
def driver(config):
    driver_instance = WebDriverSingleton(config).get_driver()
    base_url = config.get("url")
    driver_instance.get(base_url)

    yield driver_instance
    WebDriverSingleton(config).quit_driver()
