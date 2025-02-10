from faker import Faker
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage


class TestLoginPage:
    def test_login_in_account(self, driver, config, navigator):
        login_page = LoginPage(driver=driver, config=config)
        navigator.go_to_login_page()

        assert login_page.is_page_loaded(LoginPage.UNIQUE_SIGN_IN_BUTTON_LOCATOR), (
            f"Expected: The login page should be loaded with unique element {LoginPage.UNIQUE_SIGN_IN_BUTTON_LOCATOR}. "
            f"Actual: The element was not found."
        )

        fake = Faker()
        username = fake.user_name()
        password = fake.password()

        login_page.login(username, password)

        try:
            WebDriverWait(driver, config.get('timeout')).until(
                EC.visibility_of_element_located(LoginPage.ERROR_MESSAGE_LOCATOR)
            )
            actual_result = "Error message is displayed."
        except:
            actual_result = "Error message is NOT displayed."

        expected_result = "Error message is displayed."

        assert actual_result == expected_result, (
            f"Expected: {expected_result}. Actual: {actual_result}."
        )
