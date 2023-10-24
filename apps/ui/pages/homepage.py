from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ..core import driver
from ..utilities.elements import click, send, wait, explicit_wait, click_until_value, element_exists

# Locators
LOGIN_MODAL_BUTTON = (By.CSS_SELECTOR, "[data-testid='desktop-open-login-modal']")
USERNAME_INPUT = (By.ID, 'username')
PASSWORD_INPUT = (By.ID, 'password')
LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-testid="auth-submit-button"]')
INBOX_LINK = (By.ID, 'navigation-inbox-desktop-link')
RESET_SEARCH_BUTTON = (By.CSS_SELECTOR, 'div.reset-search-btn')
DATE_PICKER = (By.ID, 'search_booking_date')
SEARCH_INPUT = (By.ID, 'search-form-input')
DATEPICKER_DAYS = (By.CSS_SELECTOR, ".datepicker-days")
AVAILABLE_DATES = (By.CSS_SELECTOR, "td.day:not(.disabled)")
PERSONS_DROPDOWN = (By.CLASS_NAME, 'search-form-persons')
ADULTS_MINUS_BUTTON = 'adults-minus'
ADULTS_NUMBER = 'adults-number'
CHILDREN_MINUS_BUTTON = 'children-minus'
CHILDREN_NUMBER = 'children-number'
ADULTS_PLUS_BUTTON = (By.CLASS_NAME, 'adults-plus')
CHILDREN_PLUS_BUTTON = (By.CLASS_NAME, 'children-plus')
BODY = (By.TAG_NAME, 'body')
CHECK_AVAILABILITY_BUTTON = (By.CSS_SELECTOR, '[data-testid="desktop-search-form-submit-button"]')


def open_and_assert_login_modal():
    click(driver.instance, *LOGIN_MODAL_BUTTON)
    wait(driver.instance, *USERNAME_INPUT)


def input_login_email_address():
    send(driver.instance, *USERNAME_INPUT, 'qahiring_test@gmail.com')


def input_login_password():
    send(driver.instance, *PASSWORD_INPUT, 'qahiringtest')


def click_login_button():
    click(driver.instance, *LOGIN_BUTTON)


def confirm_login_as_successful():
    wait(driver.instance, *INBOX_LINK)


def login_as_an_angler():
    open_and_assert_login_modal()
    input_login_email_address()
    input_login_password()
    click_login_button()
    confirm_login_as_successful()


def click_reset_search_button():
    click(driver.instance, *RESET_SEARCH_BUTTON)


def click_on_date_picker():
    click(driver.instance, *DATE_PICKER)


def select_florida_as_a_destination():
    click_reset_search_button()
    send(driver.instance, By.ID, 'search-form-input', 'Florida' + ' ')
    explicit_wait(1)  # added due to firefox autocomplete
    send(driver.instance, By.ID, 'search-form-input', Keys.BACKSPACE)
    element_exists(driver.instance, By.ID, 'tt-menu')  # waits around 10 seconds for this element to be fully in frame
    send(driver.instance, By.ID, 'search-form-input', Keys.ARROW_DOWN + Keys.ENTER)


def click_first_available_date():
    datepicker = wait(driver.instance, *DATEPICKER_DAYS)
    available_dates = datepicker.find_elements(*AVAILABLE_DATES)
    if available_dates:
        available_dates[0].click()
    else:
        print("No available dates to click.")


def select_number_of_persons():
    click(driver.instance, *PERSONS_DROPDOWN)
    click_until_value(ADULTS_MINUS_BUTTON, ADULTS_NUMBER, 1)
    click_until_value(CHILDREN_MINUS_BUTTON, CHILDREN_NUMBER, 0)
    for _ in range(3):
        click(driver.instance, *ADULTS_PLUS_BUTTON)
    for _ in range(2):
        click(driver.instance, *CHILDREN_PLUS_BUTTON)
    click(driver.instance, *BODY)


def click_check_availability_button():
    click(driver.instance, *CHECK_AVAILABILITY_BUTTON)


def select_destination_date_and_number_of_persons():
    select_florida_as_a_destination()
    click_on_date_picker()
    click_first_available_date()
    select_number_of_persons()
    click_check_availability_button()
