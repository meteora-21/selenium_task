from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from conftest import ConfigReader
from faker import Faker


class Locators:
    LOGIN_BUTTON_LOCATOR = (By.XPATH, "//a[contains(@class, 'action_link')]")
    USERNAME_FIELD_LOCATOR = (By.XPATH, "//div[contains(text(), 'имя')]/following-sibling::input")
    PASSWORD_FIELD_LOCATOR = (By.XPATH, "//input[@type = 'password']")
    UNIQUE_SIGN_IN_BUTTON_LOCATOR = (By.XPATH, "//button[@type = 'submit']")
    ERROR_MESSAGE_LOCATOR = (By.XPATH,
                             "//button[contains(text(), 'Sign in') or contains(text(), 'Войти')]/ancestor::div[1]/following-sibling::div[1]")
    UNIQUE_ELEMENT_HOME = (By.XPATH, "//div[contains(@class, 'promo')]")


def is_page_loaded(driver, locator, timeout):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        return True
    except TimeoutException:
        return False


def test_login_steam(driver):
    config = ConfigReader("config.json")
    timeout = config.get("timeout")
    BASE_URL = config.get("url")

    driver.get(BASE_URL)
    if not is_page_loaded(driver, Locators.UNIQUE_ELEMENT_HOME, timeout):
        raise AssertionError("The main page did not load: the unique element was not found.")

    wait = WebDriverWait(driver, timeout)
    wait.until(EC.element_to_be_clickable(Locators.LOGIN_BUTTON_LOCATOR)).click()
    if not is_page_loaded(driver, Locators.UNIQUE_SIGN_IN_BUTTON_LOCATOR, timeout):
        raise AssertionError("The login page did not load: the unique element was not found.")

    fake = Faker()

    username_field = wait.until(EC.visibility_of_element_located(Locators.USERNAME_FIELD_LOCATOR))
    username_field.send_keys(fake.user_name())
    password_field = wait.until(EC.visibility_of_element_located(Locators.PASSWORD_FIELD_LOCATOR))
    password_field.send_keys(fake.password())

    wait.until(EC.element_to_be_clickable(Locators.UNIQUE_SIGN_IN_BUTTON_LOCATOR)).click()

    error_message = wait.until(EC.visibility_of_element_located(Locators.ERROR_MESSAGE_LOCATOR))
    assert error_message.is_displayed(), (
        f"Error message is not displayed. Expected: visible error message. "
        f"Actual: element not visible or missing."
    )
