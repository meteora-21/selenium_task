from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from conftest import ConfigReader
from faker import Faker


class WaitTest:
    def __call__(self, driver):
        return driver.execute_script("return document.readyState") == "complete"


def test_login_steam(driver):
    LOGIN_BUTTON_LOCATOR = (By.XPATH, "//a[contains(@class, 'action_link')]")
    USERNAME_FIELD_LOCATOR = (By.XPATH, "//div[contains(text(), 'имя')]/following-sibling::input")
    PASSWORD_FIELD_LOCATOR = (By.XPATH, "//input[@type = 'password']")
    SIGN_IN_BUTTON_LOCATOR = (By.XPATH, "//button[@type = 'submit']")
    ERROR_MESSAGE_LOCATOR = (By.XPATH, "//div[@class = '_1W_6HXiG4JJ0By1qN_0fGZ']")

    config = ConfigReader("config.json")
    timeout = config.get("timeout", 10)
    BASE_URL = config.get("url")

    driver.get(BASE_URL)

    wait = WebDriverWait(driver, timeout)
    wait.until(WaitTest())

    wait.until(EC.element_to_be_clickable(LOGIN_BUTTON_LOCATOR)).click()
    wait.until(WaitTest())

    # wait.until(EC.url_contains('login'))
    # assert 'login' in driver.current_url, 'The login page did not load as expected.'

    username_field = wait.until(EC.visibility_of_element_located(USERNAME_FIELD_LOCATOR))
    password_field = wait.until(EC.visibility_of_element_located(PASSWORD_FIELD_LOCATOR))

    fake = Faker()
    username_field.send_keys(fake.user_name())
    password_field.send_keys(fake.password())
    wait.until(EC.element_to_be_clickable(SIGN_IN_BUTTON_LOCATOR)).click()

    error_message = wait.until(EC.visibility_of_element_located(ERROR_MESSAGE_LOCATOR))
    assert error_message.is_displayed(), "Error message is not displayed"
