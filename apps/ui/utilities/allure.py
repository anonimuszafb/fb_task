import allure
from urllib3.exceptions import MaxRetryError
from allure_commons.types import AttachmentType
from ..core import driver


def attach_screenshot(web_driver: driver, name: str = '') -> None:
    try:
        allure.attach(web_driver.get_screenshot_as_png(), name=name, attachment_type=AttachmentType.PNG)
    except MaxRetryError:
        pass
