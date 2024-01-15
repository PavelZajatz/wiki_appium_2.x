import base64
import fnmatch
import os
import sys
import uuid
from pathlib import Path

import allure
import pytest
from allure_commons.types import AttachmentType
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

sys.path.append(os.path.abspath('.'))

os.environ['PLATFORM'] = "mobile"


def get_android_capabilities(device_name, udid):
    for apk in os.listdir('mobile/tests/builds'):
        if fnmatch.fnmatch(apk, '*.apk'):
            android_build_path = "/builds/" + apk
            this_file = Path(__file__).parent
            get_apk_file = str(this_file) + android_build_path
            capabilities = {
                "platformName": "android",
                "deviceName": device_name,
                "app": str(get_apk_file),
                "fullReset": True,
                "newCommandTimeout": 3000,
                "skipServerInstallation": False,
                "automationName": "UiAutomator2",
                "androidDeviceReadyTimeout": 60,
                "udid": udid,
                "adbExecTimeout": 60000,
                "appWaitActivity": "org.wikipedia.*",
                "ignoreHiddenApiPolicyError": True,
                "enforceAppInstall": True,
                "maxInstances": 1,
                "unicodeKeyboard": True,
                "resetKeyboard": True
            }
            print(type(capabilities))
            return capabilities


def get_ios_capabilities(device_name, platform_version):
    for app in os.listdir('mobile/tests/builds'):
        if fnmatch.fnmatch(app, '*.app'):
            ios_build_path = "/builds/" + app
            this_file = Path(__file__).parent
            get_app_file = str(this_file) + ios_build_path
            full_reset = True
            return {
                "platformName": "iOS",
                "deviceName": device_name.replace("_", " "),
                "platformVersion": platform_version,
                "automationName": "XCUITest",
                "app": str(get_app_file),
                "connectHardwareKeyboard": True,
                "autoAcceptAlerts": True,
                "newCommandTimeout": 3000,
                "fullReset": full_reset,
                "forceSimulatorSoftwareKeyboardPresence": False,
                "wdaLocalPort": 8100
            }


@pytest.fixture(scope='function', autouse=True)
def driver(request, driver_value, device_name, udid, appium_port, platform_version):
    grid_url = f"http://localhost:{appium_port}"
    os.environ['OS'] = "android"
    capabilities = get_android_capabilities(device_name=device_name, udid=udid)
    options = UiAutomator2Options().load_capabilities(capabilities)
    if driver_value == "ios_driver":
        os.environ['OS'] = "ios"
        capabilities = get_ios_capabilities(device_name=device_name, platform_version=platform_version)
        options = XCUITestOptions().load_capabilities(capabilities)
    driver = webdriver.Remote(grid_url, options=options)
    request.cls.driver = driver
    if "android" in capabilities['platformName']:
        driver.start_recording_screen()
    else:
        driver.start_recording_screen(videoType="mpeg4", videoQuality="low")
    yield driver


def pytest_addoption(parser):
    parser.addoption('--driver_value', action='store', default='android_driver', dest='driver_value')
    parser.addoption('--device_name', action='store', default='RMX2001', dest='device_name')
    parser.addoption('--udid', action='store', default='MFD6HUBAT47PXGUW', dest='udid')
    parser.addoption('--appium_port', action='store', default="4723", dest='appium_port')
    parser.addoption('--platform_version', action='store', default="11.0", dest='platform_version')


@pytest.fixture(scope='class')
def driver_value(request):
    return request.config.getoption("--driver_value")


@pytest.fixture(scope='class')
def platform_version(request):
    return request.config.getoption("--platform_version")


@pytest.fixture(scope='class')
def device_name(request):
    return request.config.getoption("--device_name")


@pytest.fixture(scope='class')
def udid(request):
    return request.config.getoption("--udid")


@pytest.fixture(scope='class')
def appium_port(request):
    return request.config.getoption("--appium_port")


@pytest.fixture(scope='function', autouse=True)
def close_driver_after_tests(request, driver):
    yield
    allure.attach(driver.get_screenshot_as_png(), name=request.node.originalname + "_Failed_Screenshot",
                  attachment_type=AttachmentType.PNG)
    allure.attach(base64.b64decode(driver.stop_recording_screen()), request.node.originalname + "_Failed_Record.mp4",
                  attachment_type=AttachmentType.MP4)
    driver.quit()


@pytest.fixture()
def platform(request):
    platform = request.cls.driver.capabilities['platformName']
    return platform


@pytest.fixture(autouse=True)
def skip_by_platform(request, platform):
    pytest_markers = request.node.own_markers
    for marker in pytest_markers:
        if marker.name == 'skip_by_platform' and marker.args[0] == platform:
            pytest.skip('Skipped on this platform: {}'.format(platform))


@pytest.fixture()
def exit_test_on_failure(request):
    yield
    if request.session.testsfailed > 0:
        pytest.exit('Exiting pytest because of failure')


@pytest.fixture(scope="session")
def testrun_uid(request):
    """Return the unique id of the current test."""
    if hasattr(request.config, "workerinput"):
        return request.config.workerinput["testrunuid"]
    else:
        return uuid.uuid4().hex


@pytest.fixture(autouse=True)
def set_report_name(driver_value: str, request, testrun_uid):
    os.environ[
        'PARAMETERS'] = f"{os.getenv('PLATFORM')} {os.getenv('ENVIRONMENT')} {driver_value.replace('_driver', '')}"
    setattr(request.node, "test_run", testrun_uid)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        setattr(item, "rep_outcome", rep.outcome)
    else:
        setattr(item, "rep_outcome", "")
