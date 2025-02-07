from pages.search_page import SearchPage
import pytest


@pytest.fixture
def search_page(driver, config):
    page = SearchPage(driver=driver, config=config)
    page.open()
    yield page

    driver.quit()


class TestSearchPage:
    @pytest.mark.parametrize('game, n', [('The Witcher', 10), ('Fallout', 20)])
    def test_search(self, search_page, game, n):
        assert search_page.is_page_loaded(
            search_page.HOME_PAGE_LOCATOR), "The home page did not load: the unique element was not found."
        assert search_page.is_element_visible(search_page.SEARCH_BAR), "Search bar is not visible on the page."

        search_page.search_game(game)
        assert search_page.is_element_visible(
            search_page.UNIQUE_SEARCH_ELEMENT), "The home page did not load: the unique element was not found."
        search_page.sort_by_highest()
        search_page.wait_background()
        assert search_page.is_sorted_by_highest(n), "The games are not sorted by highest price."
        search_page.get_n_games(n)
