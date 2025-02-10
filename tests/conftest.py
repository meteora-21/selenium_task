import pytest
import os
from utils.singleton import WebDriverSingleton
from utils.config_reader import ConfigReader
from utils.navigator import Navigator


@pytest.fixture(scope="session")
def config():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../utils/config.json"))
    return ConfigReader(config_path)


@pytest.fixture(scope="function")
def driver(config):
    driver_instance = WebDriverSingleton(config).get_driver()

    yield driver_instance
    WebDriverSingleton(config).quit_driver()


@pytest.fixture
def navigator(driver, config):
    return Navigator(driver, config)
