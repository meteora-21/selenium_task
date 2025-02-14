from pages.search_page import SearchPage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

from tests.conftest import driver


class TestSearchPage:
    @pytest.mark.parametrize('game, n', [('The Witcher', 10), ('Fallout', 20)])
    def test_search(self, driver, config, game, n):
        search_page = SearchPage(driver=driver, config=config)
        url = config.get('base_url')
        driver.get(url)
        assert search_page.is_page_loaded(search_page.HOME_PAGE_LOCATOR), (
            f"Expected: The home page should load with unique element {search_page.HOME_PAGE_LOCATOR}. "
            f"Actual: The element was not found."
        )

        WebDriverWait(search_page.driver, search_page.config.get('timeout')).until(
            EC.visibility_of_element_located(search_page.SEARCH_BAR)
        )

        search_page.search_game(game)

        assert search_page.is_page_loaded(search_page.UNIQUE_SEARCH_ELEMENT), (
            f"Expected: The search results page should load with unique element {search_page.UNIQUE_SEARCH_ELEMENT}. "
            f"Actual: The element was not found."
        )

        search_page.sort_by_highest()
        search_page.wait_background()

        prices = search_page.get_prices(n)
        is_sorted = prices == sorted(prices, reverse=True)
        assert is_sorted, (
            f"Expected: The first {n} games should be sorted by highest price. "
            f"Actual: The sorting order is incorrect."
        )
