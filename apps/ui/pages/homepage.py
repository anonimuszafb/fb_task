from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ..core import driver
from ..utilities.elements import click, send, wait, explicit_wait, click_until_value, element_exists


def open_and_assert_login_modal():
    click(driver.instance, By.CSS_SELECTOR, "[data-testid='desktop-open-login-modal']")
    wait(driver.instance, By.ID, 'username')


def input_login_email_address():
    send(driver.instance, By.ID, 'username', 'qahiring_test@gmail.com')


def input_login_password():
    send(driver.instance, By.ID, 'password', 'qahiringtest')


def click_login_button():
    click(driver.instance, By.CSS_SELECTOR, '[data-testid="auth-submit-button"]')


def confirm_login_as_successful():
    wait(driver.instance, By.ID, 'navigation-inbox-desktop-link')


def login_as_an_angler():
    open_and_assert_login_modal()
    input_login_email_address()
    input_login_password()
    click_login_button()
    confirm_login_as_successful()


def click_reset_search_button():
    click(driver.instance, By.CSS_SELECTOR, 'div.reset-search-btn')


def click_on_date_picker():
    click(driver.instance, By.ID, 'search_booking_date')


def select_florida_as_a_destination():
    click_reset_search_button()
    send(driver.instance, By.ID, 'search-form-input', 'Florida' + ' ')
    explicit_wait(1)  # added due to firefox autocomplete
    send(driver.instance, By.ID, 'search-form-input', Keys.BACKSPACE)
    element_exists(driver.instance, By.ID, 'tt-menu')  # waits around 10 seconds for this element to be fully in frame
    send(driver.instance, By.ID, 'search-form-input', Keys.ARROW_DOWN + Keys.ENTER)


def click_first_available_date():
    datepicker = wait(driver.instance, By.CSS_SELECTOR, ".datepicker-days")
    available_dates = datepicker.find_elements(By.CSS_SELECTOR, "td.day:not(.disabled)")
    if available_dates:
        available_dates[0].click()
    else:
        print("No available dates to click.")


def select_number_of_persons():
    click(driver.instance, By.CLASS_NAME, 'search-form-persons')
    click_until_value('adults-minus', 'adults-number', 1)
    click_until_value('children-minus', 'children-number', 0)
    for _ in range(3):
        click(driver.instance, By.CLASS_NAME, 'adults-plus')
    for _ in range(2):
        click(driver.instance, By.CLASS_NAME, 'children-plus')
    click(driver.instance, By.TAG_NAME, 'body')


def click_check_availability_button():
    click(driver.instance, By.CSS_SELECTOR, '[data-testid="desktop-search-form-submit-button"]')


def select_destination_date_and_number_of_persons():
    select_florida_as_a_destination()
    click_on_date_picker()
    click_first_available_date()
    select_number_of_persons()
    click_check_availability_button()
