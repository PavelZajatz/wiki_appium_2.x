from mobile.tests.common.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy as MobileBy
from helpers.allure_helper import step


class OnboardingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    """Start Page Locators"""

    skip_btn = (MobileBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_skip_button')

    @step
    def skip_btn_is_displayed(self):
        return self.is_present(self.skip_btn)

    @step
    def tap_skip_btn(self):
        return self.click(self.skip_btn)
