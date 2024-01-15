from mobile.tests.common.base_page import BasePage
from helpers.allure_helper import step
from helpers.locator_helper import *


class ExplorePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    """Start Page Locators"""

    search_field = locator([by_accessibility_id('Search Wikipedia')])
    search_text = locator([by_accessibility_id('Search Wikipedia'), by_id('org.wikipedia.alpha:id/search_src_text')])
    search_result = locator([by_xpath("//*[contains(@name, 'Appi')]"),
                             by_id('org.wikipedia.alpha:id/page_list_item_title')])

    @step
    def tap_search_field(self):
        return self.click(self.search_field)

    @step
    def perform_search_text(self, text):
        return self.enter_text(self.search_text, text)

    @step
    def count_search_result(self):
        return self.find_elements(self.search_result)
