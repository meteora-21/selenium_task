from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.parsing import extract_price


class SearchPage(BasePage):
    SORT_BUTTON = (By.ID, "sort_by_trigger")
    SORT_BY_HIGHEST = (By.ID, "Price_DESC")
    SEARCH_BAR = (By.ID, "store_nav_search_term")
    SEARCH_BUTTON = (By.XPATH, "//*[@class = 'searchbox']//img")
    GAME_TITLES = (By.XPATH, "//span[contains(@class, 'title')]")
    PRICE_LOCATOR = (By.XPATH, "//*[@class='discount_final_price']")
    FIRST_GAME_LOCATOR = (By.XPATH, "(//*[@class = 'discount_final_price'])[1]")
    UNIQUE_SEARCH_ELEMENT = (By.CLASS_NAME, "search_results_filtered_warning")

    def enter_game_name(self, game: str):
        search_bar = self.wait.until(EC.visibility_of_element_located(self.SEARCH_BAR))
        search_bar.clear()
        search_bar.send_keys(game)

    def click_search(self):
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON)).click()

    def search_game(self, game: str):
        self.enter_game_name(game)
        self.click_search()

    def sort_by_highest(self):
        self.wait.until(EC.element_to_be_clickable(self.SORT_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.SORT_BY_HIGHEST)).click()

    def wait_background(self):
        poll_frequency = self.config.get('poll_frequency')
        timeout = self.config.get('timeout')
        first_element = self.wait.until(EC.presence_of_element_located(self.FIRST_GAME_LOCATOR))
        WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency).until(
            EC.presence_of_element_located(self.FIRST_GAME_LOCATOR))
        self.wait.until(EC.staleness_of(first_element))

    def get_prices(self, n):
        price_elements = self.wait.until(EC.presence_of_all_elements_located(self.PRICE_LOCATOR))
        prices = [extract_price(el.text.strip()) for el in price_elements[:n]]
        return prices

    def get_n_games(self, n):
        games_titles = self.wait.until(EC.presence_of_all_elements_located(self.GAME_TITLES))
        games = []

        for game in games_titles[:n]:
            games.append(game.text)

        return games
