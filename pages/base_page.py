from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class BasePage:
    LOGIN_BUTTON_LOCATOR = (By.CLASS_NAME, "global_action_link")
    HOME_PAGE_LOCATOR = (By.XPATH, "//*[@class = 'supernav_container']/a[contains(@class, 'supernav_active')]")

    def __init__(self, driver, config=None):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.get('timeout', 10))
        self.config = config

    def open(self):
        self.driver.get(self.PAGE_URL)

    def is_element_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_page_loaded(self, unique_element_locator):
        return self.is_element_visible(unique_element_locator)

    def click(self, locator: tuple):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator: tuple, text: str):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
