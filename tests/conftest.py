import pytest
import os
from utils.singleton import WebDriverSingleton
from utils.config_reader import ConfigReader


@pytest.fixture(scope="session")
def config():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, "..", "utils", "config.json")
    return ConfigReader(config_path)


@pytest.fixture(scope="function")
def driver(config):
    driver_instance = WebDriverSingleton(config).get_driver()

    yield driver_instance
    WebDriverSingleton(config).quit_driver()
