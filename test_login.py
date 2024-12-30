from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_login_steam(driver):
    wait = WebDriverWait(driver, 15, poll_frequency=1)

    driver.get("https://store.steampowered.com/")
    url = driver.current_url
    assert url == 'https://store.steampowered.com/', 'URL-Error'

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
