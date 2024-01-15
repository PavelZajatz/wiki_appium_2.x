from mobile.tests.common.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy as MobileBy
from helpers.allure_helper import step


class ExplorePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    """Start Page Locators"""

    search_field = (MobileBy.ACCESSIBILITY_ID, 'Search Wikipedia')
    search_text = (MobileBy.ID, 'org.wikipedia.alpha:id/search_src_text')
    search_result = (MobileBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')

    @step
    def tap_search_field(self):
        return self.click(self.search_field)

    @step
    def perform_search_text(self, text):
        return self.enter_text(self.search_text, text)

    @step
    def count_search_result(self):
        return self.find_elements(self.search_result)
