from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    LOGIN_BUTTON_LOCATOR = (By.XPATH, "//a[contains(@class, 'global_action')]")
    HOME_PAGE_LOCATOR = (By.XPATH, "//*[contains(@class, 'container')]//a[contains(@class, 'supernav_active')]")

    def __init__(self, driver, config=None):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.get('timeout'))
        self.config = config

    def is_page_loaded(self, unique_element_locator):
        try:
            self.wait.until(EC.visibility_of_element_located(unique_element_locator))
            return True
        except TimeoutException:
            return False
