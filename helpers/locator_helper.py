import os

from appium.webdriver.common.appiumby import AppiumBy as MobileBy


def by_accessibility_id(_id):
    return MobileBy.ACCESSIBILITY_ID, _id


def by_css(_id):
    return MobileBy.CSS_SELECTOR, _id


def by_xpath(_id):
    return MobileBy.XPATH, _id


def by_name(_id):
    return MobileBy.NAME, _id


def by_id(_id):
    return MobileBy.ID, _id


def by_class_name(_id):
    return MobileBy.CLASS_NAME, _id


def by_class_chain(class_chain):
    return MobileBy.IOS_CLASS_CHAIN, class_chain


def by_ios_predicate_string(predicate_string):
    return MobileBy.IOS_PREDICATE, predicate_string


def locator(element: list):
    """
    Returns locator for iOS or Android

    Parameters:
    element (list): first lists value - iOS locator, second lists value = Android locator

    Returns:
    if list consists 2 values  - returns first value if Env is ios or second for android, returns first value if
    list consists only 1 value
    """
    if len(element) == 1:
        return element[0]
    elif len(element) == 2:
        if os.environ.get('OS') == "ios":
            return element[0]
        else:
            return element[1]
