from mobile.tests.common.base_test import BaseTest
import pytest

from mobile.tests.pages.explore_page import ExplorePage
from mobile.tests.pages.onboarding_page import OnboardingPage


class TestSearch(BaseTest):

    @pytest.fixture(autouse=True)
    def driver_parse(self):
        self.start_page = OnboardingPage(self.driver)
        self.explore_page = ExplorePage(self.driver)

    def test_search_results(self):
        self.start_page.skip_btn_is_displayed()
        self.start_page.tap_skip_btn()
        self.explore_page.tap_search_field()
        self.explore_page.perform_search_text("Appium")
        results = self.explore_page.count_search_result()
        assert len(results) >= 1, f"Should be more or equal to 1 search results, shown - len(results)"

    def test_max_search_results_negative_test(self):
        self.start_page.skip_btn_is_displayed()
        self.start_page.tap_skip_btn()
        self.explore_page.tap_search_field()
        self.explore_page.perform_search_text("Appium")
        results = self.explore_page.count_search_result()
        assert len(results) >= 1000, f"Should be more or equal to 1000 search results, shown - len(results)"
