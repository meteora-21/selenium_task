from faker import Faker
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage


class TestLoginPage:
    def test_login_in_account(self, driver, config):
        login_page = LoginPage(driver=driver, config=config)
        url = config.get('login_page')
        driver.get(url)

        assert login_page.is_page_loaded(LoginPage.UNIQUE_SIGN_IN_BUTTON_LOCATOR), (
            f"Expected: The login page should be loaded with unique element {LoginPage.UNIQUE_SIGN_IN_BUTTON_LOCATOR}. "
            f"Actual: The element was not found."
        )

        fake = Faker()
        username = fake.user_name()
        password = fake.password()

        login_page.login(username, password)

        def is_error_message_visible():
            try:
                WebDriverWait(driver, config.get('timeout')).until(
                    EC.visibility_of_element_located(LoginPage.ERROR_MESSAGE_LOCATOR)
                )
                return True
            except:
                return False

        is_visible = is_error_message_visible()

        expected_result = True
        assert is_visible == expected_result, (
            f"Expected: Error message should be visible. Actual: Error message is {'not ' if not is_visible else ''}displayed."
        )
