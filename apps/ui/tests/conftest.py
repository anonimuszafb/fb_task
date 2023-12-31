import pytest
import sys
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from urllib.parse import urlparse, urlunparse
from ..core import driver
from ..utilities.allure import attach_screenshot
from ..utilities.elements import click, send

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="https://fishingbooker.com", help="URL for the test")
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use for tests")


@pytest.fixture(autouse=True)
def setup(url, request):
    browser = request.config.getoption('--browser')
    driver.initialize(browser)

    if url != "https://fishingbooker.com":
        parsed_url = list(urlparse(url))
        parsed_url[1] = 'fishingbooker:QAFBTest@' + parsed_url[1]
        url = urlunparse(parsed_url)

    driver.instance.get(url)
    driver.instance.maximize_window()
    try:
        WebDriverWait(driver.instance, 3).until(ec.url_to_be('https://fishingbooker.com'))
    except TimeoutException:
        pass
    yield
    attach_screenshot(driver.instance, 'Test Done')
    driver.quit_driver()


@pytest.fixture(scope='class', autouse=True)
def url(request):
    return request.config.getoption('--url')
