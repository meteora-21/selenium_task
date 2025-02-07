from faker import Faker
from pages.login_page import LoginPage


class TestLoginPage:
    def setup_method(self):
        self.login_page = None

    def teardown_method(self):
        if self.login_page:
            self.login_page.driver.quit()

    def test_login_in_account(self, driver, config):
        self.login_page = LoginPage(driver=driver, config=config)
        self.login_page.open()

        assert self.login_page.is_page_loaded(LoginPage.UNIQUE_SIGN_IN_BUTTON_LOCATOR), (
            "The login page did not load: the unique element was not found."
        )

        fake = Faker()

        username = fake.user_name()
        password = fake.password()

        self.login_page.login(username, password)

        assert self.login_page.is_element_visible(LoginPage.ERROR_MESSAGE_LOCATOR), (
            f"Error message is not displayed. Expected: visible error message. "
            f"Actual: element not visible or missing."
        )
