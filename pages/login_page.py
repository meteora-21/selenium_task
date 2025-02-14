from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    USERNAME_FIELD_LOCATOR = (
        By.XPATH, "//*[contains(text(), 'имя') or contains(text(), 'name')]//following-sibling::input")
    PASSWORD_FIELD_LOCATOR = (By.XPATH, "//*[@type = 'password']")
    UNIQUE_SIGN_IN_BUTTON_LOCATOR = (By.XPATH, "//button[@type = 'submit']")
    ERROR_MESSAGE_LOCATOR = (By.XPATH,
                             "//button[contains(text(), 'Sign in') or contains(text(), 'Войти')]//..//following-sibling::div[1]")

    def enter_login(self, username):
        username_field = self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD_LOCATOR))
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password: str):
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD_LOCATOR))
        password_field.clear()
        password_field.send_keys(password)

    def click_sign_in(self):
        self.wait.until(EC.element_to_be_clickable(self.UNIQUE_SIGN_IN_BUTTON_LOCATOR)).click()

    def login(self, username: str, password: str):
        self.enter_login(username)
        self.enter_password(password)
        self.click_sign_in()
