from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import re


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
        self.enter_text(self.SEARCH_BAR, game)

    def click_search(self):
        self.click(self.SEARCH_BUTTON)

    def search_game(self, game: str):
        self.enter_game_name(game)
        self.click_search()

    def sort_by_highest(self):
        self.click(self.SORT_BUTTON)
        self.click(self.SORT_BY_HIGHEST)

    def wait_background(self):
        first_element = self.wait.until(EC.presence_of_element_located(self.FIRST_GAME_LOCATOR))
        WebDriverWait(self.driver, 2, poll_frequency=0.1).until(EC.presence_of_element_located(self.FIRST_GAME_LOCATOR))
        self.wait.until(EC.staleness_of(first_element))

    def is_sorted_by_highest(self, n):
        price_elements = self.wait.until(EC.presence_of_all_elements_located(self.PRICE_LOCATOR))

        prices = []
        for element in price_elements[:n]:
            price_text = element.text.strip()

        price_match = re.search(r"\d+[\d\s]*[,.]?\d*", price_text)
        if price_match:
            price_value = float(price_match.group().replace(" ", "").replace(",", "."))
            prices.append(price_value)

        sorted_prices = sorted(prices, reverse=True)
        return prices

    def get_n_games(self, n):
        games_titles = self.wait.until(EC.presence_of_all_elements_located(self.GAME_TITLES))
        games = []

        for game in games_titles[:n]:
            games.append(game.text)

        return games
