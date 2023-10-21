from selenium.webdriver import Remote
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time


def find(
        web_driver: Remote,
        by: str,
        selector_name: str,
        fail_on_timeout: bool = True,
        time_to_wait: int = 30
) -> None:
    try:
        WebDriverWait(web_driver, time_to_wait, poll_frequency=1).until(
            ec.presence_of_element_located((by, selector_name))
        )
    except TimeoutException:
        if fail_on_timeout:
            assert False


def click(
        web_driver: Remote,
        by: str,
        selector: str,
        time_to_wait: int = 30) -> None:
    try:
        WebDriverWait(web_driver, time_to_wait, poll_frequency=1).until(
            ec.element_to_be_clickable((by, selector))
        ).click()
    except TimeoutException:
        pass


def send(
        web_driver: Remote,
        by: str,
        selector: str,
        keys: str,
        time_to_wait: int = 30
) -> None:
    try:
        element = WebDriverWait(web_driver, time_to_wait, poll_frequency=1).until(
            ec.element_to_be_clickable((by, selector))
        )
        element.clear()
        element.send_keys(keys)
    except TimeoutException:
        pass


def wait(
        web_driver: Remote,
        by: str,
        selector: str,
        fail_on_timeout: bool = True,
        time_to_wait: int = 30
) -> None:
    try:
        WebDriverWait(web_driver, time_to_wait, poll_frequency=1).until(
            ec.visibility_of_element_located((by, selector))
        )
    except TimeoutException:
        if fail_on_timeout:
            assert False


def wait_for_invisibility(
        web_driver: Remote,
        by: str,
        selector: str,
        fail_on_timeout: bool = True,
        time_to_wait: int = 30
) -> None:
    try:
        WebDriverWait(web_driver, time_to_wait, poll_frequency=1).until(
            ec.invisibility_of_element_located((by, selector))
        )
    except TimeoutException:
        if fail_on_timeout:
            assert False


def scroll(
        web_driver: Remote,
        by: str,
        selector: str,
        time_to_wait: int = 30
) -> None:
    try:
        element = WebDriverWait(web_driver, time_to_wait, poll_frequency=1).until(
            ec.presence_of_element_located((by, selector))
        )
        web_driver.execute_script("arguments[0].scrollIntoView(true);", element)
    except TimeoutException:
        print("Element not found to scroll into view.")


def element_exists(
        web_driver: Remote,
        by: str,
        selector: str,
        time_to_wait: int = 30
) -> bool:
    try:
        WebDriverWait(web_driver, time_to_wait, poll_frequency=1).until(
            ec.presence_of_element_located((by, selector))
        )
        return True
    except TimeoutException:
        return False


def element_is_clickable(
        web_driver: Remote,
        by: str,
        selector: str,
        time_to_wait: int = 30
) -> bool:
    try:
        WebDriverWait(web_driver, time_to_wait, poll_frequency=1).until(
            ec.element_to_be_clickable((by, selector))
        )
        return True
    except TimeoutException:
        return False


def explicit_wait(seconds: int) -> None:
    time.sleep(seconds)
