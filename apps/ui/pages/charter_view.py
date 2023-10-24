from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..core import driver
from ..utilities.elements import click, send, wait, scroll, explicit_wait, element_exists
from ..utilities.windows import switch_to_window_by_index
from ..utilities.faker import generate_random_message


def click_on_message_captain():
    switch_to_window_by_index(1)
    scroll(driver.instance, By.ID, 'contact-captain')
    element = driver.instance.find_element(By.ID, 'contact-captain')
    driver.instance.execute_script("arguments[0].click();", element)


def click_date_field():
    click(driver.instance, By.ID, 'cf-trip-date')


def open_datepicker():
    date_field = driver.instance.find_element(By.ID, 'cf-trip-date')
    driver.instance.execute_script("arguments[0].click();", date_field)


def select_last_available_day():
    max_attempts = 12
    attempts = 0

    while attempts < max_attempts:
        open_datepicker()
        select_last_date_of_month()

        if check_date_availability():
            return
        else:
            go_to_next_month()
            attempts += 1


def select_last_date_of_month():
    retries = 5
    for attempt in range(retries):
        try:
            date_table = WebDriverWait(driver.instance, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".rdtPicker tbody"))
            )
            rows = date_table.find_elements(By.TAG_NAME, "tr")

            for row in reversed(rows):
                dates = row.find_elements(By.TAG_NAME, "td")
                current_month_dates = [date for date in dates if "rdtNew" not in date.get_attribute("class")]

                for date in reversed(current_month_dates):
                    if "rdtDisabled" not in date.get_attribute("class"):
                        driver.instance.execute_script("arguments[0].scrollIntoView();", date)
                        WebDriverWait(driver.instance, 15).until(EC.element_to_be_clickable(date))
                        date.click()
                        return

        except StaleElementReferenceException:
            explicit_wait(1)


def check_date_availability():
    not_available_locator = (By.CSS_SELECTOR, ".media-body strong")
    available_locator = (By.CSS_SELECTOR, ".already-booked")

    wait = WebDriverWait(driver.instance, 5)

    try:
        wait.until(EC.visibility_of_element_located(not_available_locator))
        return False
    except:
        pass

    try:
        wait.until(EC.visibility_of_element_located(available_locator))
        return True
    except:
        pass

    return False


def go_to_next_month():
    open_datepicker()
    next_button = driver.instance.find_element(By.CLASS_NAME, "rdtNext")
    driver.instance.execute_script("arguments[0].click();", next_button)


def select_group_size():
    click(driver.instance, By.ID, 'cf-group-size')
    dropdown = driver.instance.find_element(By.ID, "cf-group-size")
    select = Select(dropdown)
    select.select_by_value("2")


def select_last_package():
    click(driver.instance, By.ID, 'cf-packages')
    explicit_wait(2)
    dropdown = driver.instance.find_element(By.ID, "cf-packages")
    select = Select(dropdown)
    select.select_by_index(len(select.options) - 1)


def message_captain():
    send(driver.instance, By.ID, 'contact-textarea', generate_random_message())
    click(driver.instance, By.XPATH, '//button[contains(text(),"Send Message")]')


def assert_message_sent():
    wait(driver.instance, By.XPATH, '//b[contains(text(),"Message Sent")]')


def create_new_inquiry():
    click(driver.instance, By.XPATH, '//button[contains(text(),"Create new inquiry")]')


def select_available_date_for_package_and_message_captain():
    click_on_message_captain()
    create_new_inquiry()
    select_group_size()
    select_last_package()
    click_date_field()
    select_last_available_day()
    message_captain()
    assert_message_sent()
