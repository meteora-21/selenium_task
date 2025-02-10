from pages.search_page import SearchPage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


@pytest.fixture
def search_page(driver, config, navigator):
    navigator.go_to_home_page()
    page = SearchPage(driver=driver, config=config)
    yield page


class TestSearchPage:
    @pytest.mark.parametrize('game, n', [('The Witcher', 10), ('Fallout', 20)])
    def test_search(self, search_page, game, n):
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

        search_page.get_n_games(n)

        is_sorted = search_page.is_sorted_by_highest(n)
        assert is_sorted, (
            f"Expected: The first {n} games should be sorted by highest price. "
            f"Actual: The sorting order is incorrect."
        )
