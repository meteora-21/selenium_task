from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import ConfigReader

class WaitTest:
    def __call__(self, driver):
        return driver.execute_script("return document.readyState") == "complete"

def test_login_steam(driver):
    config = ConfigReader("config.json")
    timeout = config.get("timeout", 10)

    driver.get("https://store.steampowered.com/")

    wait = WebDriverWait(driver, timeout)
    wait.until(WaitTest())

    login_button = wait.until(EC.element_to_be_clickable(("xpath", "//a[contains(@class, 'action_link')]")))
    login_button.click()

    wait.until(EC.url_contains('login'))
    assert 'login' in driver.current_url, 'The login page did not load as expected.'

    username_field = wait.until(
        EC.visibility_of_element_located(("xpath", "//div[contains(text(), 'имя')]/following-sibling::input")))
    password_field = wait.until(EC.visibility_of_element_located(("xpath", "//input[@type = 'password']")))

    username_field.send_keys('random_username')
    password_field.send_keys('random_password')

    sign_in_button = wait.until(EC.element_to_be_clickable(("xpath", "//button[@type = 'submit']")))
    sign_in_button.click()

    error_message = wait.until(EC.visibility_of_element_located(("xpath", "//div[@class = '_1W_6HXiG4JJ0By1qN_0fGZ']")))
    assert error_message.is_displayed(), "Error message is not displayed"