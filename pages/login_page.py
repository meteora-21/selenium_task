from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    USERNAME_FIELD_LOCATOR = (
        By.XPATH, "//*[contains(text(), 'имя') or contains(text(), 'name')]//following-sibling::input")
    PASSWORD_FIELD_LOCATOR = (By.XPATH, "//*[@type = 'password']")
    UNIQUE_SIGN_IN_BUTTON_LOCATOR = (By.XPATH, "//button[@type = 'submit']")
    ERROR_MESSAGE_LOCATOR = (By.XPATH,
                             "//button[contains(text(), 'Sign in') or contains(text(), 'Войти')]//..//following-sibling::div[1]")

    def enter_login(self, username):
        self.enter_text(self.USERNAME_FIELD_LOCATOR, username)

    def enter_password(self, password: str):
        self.enter_text(self.PASSWORD_FIELD_LOCATOR, password)

    def click_sign_in(self):
        self.click(self.UNIQUE_SIGN_IN_BUTTON_LOCATOR)

    def login(self, username: str, password: str):
        self.enter_login(username)
        self.enter_password(password)
        self.click_sign_in()
