from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from ..core import driver
from ..utilities.elements import click, send, wait, scroll, explicit_wait, element_exists
from ..utilities.windows import switch_to_window_by_index
from ..utilities.faker import generate_random_message

# Locators
CONTACT_CAPTAIN_LOCATOR = (By.ID, 'contact-captain')
DATE_FIELD_LOCATOR = (By.ID, 'cf-trip-date')
DATE_TABLE_LOCATOR = (By.CSS_SELECTOR, ".rdtPicker tbody")
NOT_AVAILABLE_LOCATOR = (By.CSS_SELECTOR, ".media-body strong")
ALREADY_BOOKED_LOCATOR = (By.CSS_SELECTOR, ".already-booked")
NEXT_MONTH_BUTTON_LOCATOR = (By.CLASS_NAME, "rdtNext")
GROUP_SIZE_DROPDOWN_LOCATOR = (By.ID, 'cf-group-size')
PACKAGE_DROPDOWN_LOCATOR = (By.ID, "cf-packages")
MESSAGE_TEXT_AREA_LOCATOR = (By.ID, 'contact-textarea')
SEND_MESSAGE_BUTTON_LOCATOR = (By.XPATH, '//button[contains(text(),"Send Message")]')
MESSAGE_SENT_LOCATOR = (By.XPATH, '//b[contains(text(),"Message Sent")]')
NEW_INQUIRY_BUTTON_LOCATOR = (By.XPATH, '//button[contains(text(),"Create new inquiry")]')


def click_on_message_captain():
    switch_to_window_by_index(1)
    scroll(driver.instance, *CONTACT_CAPTAIN_LOCATOR)
    element = driver.instance.find_element(*CONTACT_CAPTAIN_LOCATOR)
    driver.instance.execute_script("arguments[0].click();", element)


def click_date_field():
    click(driver.instance, *DATE_FIELD_LOCATOR)


def open_datepicker():
    date_field = driver.instance.find_element(*DATE_FIELD_LOCATOR)
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
                EC.presence_of_element_located(DATE_TABLE_LOCATOR)
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
            explicit_wait(1)  # added in case element in stale. this is just in case


def check_date_availability():
    wait = WebDriverWait(driver.instance, 5)

    try:
        wait.until(EC.visibility_of_element_located(NOT_AVAILABLE_LOCATOR))
        return False
    except TimeoutException:
        pass

    try:
        wait.until(EC.visibility_of_element_located(ALREADY_BOOKED_LOCATOR))
        return True
    except TimeoutException:
        pass

    return False


def go_to_next_month():
    open_datepicker()
    next_button = driver.instance.find_element(*NEXT_MONTH_BUTTON_LOCATOR)
    driver.instance.execute_script("arguments[0].click();", next_button)


def select_group_size():
    click(driver.instance, *GROUP_SIZE_DROPDOWN_LOCATOR)
    dropdown = driver.instance.find_element(*GROUP_SIZE_DROPDOWN_LOCATOR)
    select = Select(dropdown)
    select.select_by_value("2")


def select_last_package():
    dropdown = driver.instance.find_element(By.ID, "cf-packages")
    click(driver.instance, By.ID, 'cf-packages')
    select = Select(dropdown)
    select.select_by_index(len(select.options) - 1)


def message_captain():
    send(driver.instance, *MESSAGE_TEXT_AREA_LOCATOR, generate_random_message())
    click(driver.instance, *SEND_MESSAGE_BUTTON_LOCATOR)


def assert_message_sent():
    wait(driver.instance, *MESSAGE_SENT_LOCATOR)


def create_new_inquiry():
    click(driver.instance, *NEW_INQUIRY_BUTTON_LOCATOR)


def select_available_date_for_package_and_message_captain():
    click_on_message_captain()
    create_new_inquiry()
    select_group_size()
    select_last_package()
    click_date_field()
    select_last_available_day()
    message_captain()
    assert_message_sent()
