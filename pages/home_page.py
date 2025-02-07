from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    UNIQUE_ELEMENT_HOME = (By.CLASS_NAME, "promo_text")
