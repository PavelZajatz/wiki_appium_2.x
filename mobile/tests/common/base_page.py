from helpers.allure_helper import step
from appium.webdriver.extensions.keyboard import Keyboard
from selenium.common.exceptions import (TimeoutException, NoSuchElementException, WebDriverException,
                                        StaleElementReferenceException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @step
    def click(self, locator):
        """Clicks the specified object"""
        time.sleep(1)
        self.wait_for_element_to_be_clickable(locator)
        element = self.driver.find_element(*locator)
        element.click()

    @step
    def get_text(self, locator):
        """Gets the text of the specified object"""
        self.wait_for_element_to_be_visible(locator)
        element = self.driver.find_element(*locator)
        try:
            return element.text
        except (TimeoutException, WebDriverException, NoSuchElementException):
            return element.text

    @step
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @step
    def is_present(self, locator):
        """Returns true or False if an element is present on the screen"""
        self.wait_for_element_to_be_visible(locator)
        element = self.driver.find_element(*locator)
        return element.is_displayed()

    @step
    def is_displayed(self, locator):
        element = self.driver.find_element(*locator)
        return element.is_displayed()

    @step
    def enter_text(self, locator, keys):
        self.wait_for_element_to_be_visible(locator)
        element = self.driver.find_element(*locator)
        element.clear()
        if self.driver.desired_capabilities['platformName'] == 'android':
            element.send_keys(keys)
        else:
            element.send_keys(keys + "\n")

    @step
    def clear_text(self, locator):
        self.wait_for_element_to_be_visible(locator)
        element = self.driver.find_element(*locator)
        element.clear()

    @step
    def wait_for_element_to_be_clickable(self, locator):
        wait = WebDriverWait(self.driver, 10)
        try:
            return wait.until(EC.element_to_be_clickable(locator))
        except (TimeoutException, WebDriverException, NoSuchElementException):
            try:
                self.scroll_to_top()
                return wait.until(EC.element_to_be_clickable(locator))
            except (TimeoutException, WebDriverException, NoSuchElementException):
                self.scroll_to_bottom()
                return wait.until(EC.element_to_be_clickable(locator))

    @step
    def wait_for_element_to_be_visible(self, locator):
        wait = WebDriverWait(self.driver, 15)
        try:
            return wait.until(EC.visibility_of_element_located(locator))
        except (TimeoutException, WebDriverException, NoSuchElementException, StaleElementReferenceException):
            try:
                self.scroll_to_top()
                return wait.until(EC.visibility_of_element_located(locator))
            except (TimeoutException, WebDriverException, NoSuchElementException, StaleElementReferenceException):
                self.scroll_to_bottom()
                return wait.until(EC.visibility_of_element_located(locator))

    @step
    def scroll_to_top(self):
        time.sleep(2.5)
        action = TouchAction(self.driver)
        screen_size = self.driver.get_window_size()
        x = screen_size['width'] / 2
        start_y = screen_size['height'] * 0.3
        end_y = screen_size['height'] * 0.8
        action.press(x=x, y=start_y).wait(1500).move_to(x=x, y=end_y).release().perform()

    @step
    def scroll_to_bottom(self):
        time.sleep(2.5)
        action = TouchAction(self.driver)
        screen_size = self.driver.get_window_size()
        x = screen_size['width'] / 2
        start_y = screen_size['height'] * 0.8
        end_y = screen_size['height'] * 0.3
        action.press(x=x, y=start_y).wait(1500).move_to(x=x, y=end_y).release().perform()

    @step
    def wait_for_invisibility_of_element(self, locator, wait_time=7):
        wait = WebDriverWait(self.driver, wait_time)
        if wait.until(EC.invisibility_of_element_located(locator)):
            return True
        else:
            return False

    @step
    def hide_keyboard(self):
        time.sleep(1.5)
        if Keyboard.is_keyboard_shown(self.driver):
            return Keyboard.hide_keyboard(self.driver)

    @step
    def is_field_enabled(self, locator):
        self.wait_for_element_to_be_visible(locator)
        element = self.driver.find_element(*locator)
        return element.get_attribute("enabled")

    @step
    def swipe_to_right(self, current_locator):
        time.sleep(3)
        current_element = self.driver.find_element(*current_locator)
        action = TouchAction(self.driver)
        current_element_location = current_element.location
        end_x = current_element_location['x']
        start_x = current_element_location['x'] * 0.05
        action.press(x=end_x, y=current_element_location['y']).wait(1500).move_to(x=start_x, y=current_element_location[
            'y']).release().perform()

    @step
    def navigate_native_back(self):
        self.driver.back()
