import pytest
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ConfigReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self._load_config()

    def _load_config(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл конфигурации {self.file_path} не найден.')
        except json.JSONDecodeError:
            raise ValueError(f'Ошибка в декодировании JSON-файла {self.file_path}.')

    def get(self, key, default=None):
        return self.config.get(key, default)

    def update(self, key, value):
        self.config[key] = value
        self.save()

    def save(self):
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.config, file, indent=4)
        except Exception as e:
            raise IOError(f"Не удалось сохранить файл конфигурации: {e}")


@pytest.fixture
def driver():
    config = ConfigReader("config.json")

    chrome_options = Options()

    if config.get("window_size"):
        chrome_options.add_argument(f"--window-size={config.get('window_size')}")
    if config.get("disable_notifications"):
        chrome_options.add_argument("--disable-notifications")
    if config.get("ignore_certificate_errors"):
        chrome_options.add_argument("--ignore-certificate-errors")
    if config.get("headless"):
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()