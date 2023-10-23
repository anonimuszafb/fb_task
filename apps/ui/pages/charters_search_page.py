from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from ..core import driver
from ..utilities.elements import click, send, wait, scroll, explicit_wait, element_exists
from ..utilities.windows import switch_to_window_by_index


def select_review_score():
    scroll(driver.instance, By.XPATH, '//label[@for="4_50"]')
    explicit_wait(3)
    click(driver.instance, By.XPATH, '//label[@for="4_50"]')


def select_inshore_fishing():
    click(driver.instance, By.XPATH, '//label[@for="fishing_type_inshore"]')


def select_red_snapper():
    click(driver.instance, By.XPATH, '//label[@for="snapper_red"]')


def select_angler_requirements():
    select_review_score()
    select_inshore_fishing()
    select_red_snapper()


def click_first_anglers_choice_listing():
    wait(driver.instance, By.ID, "charter-list-container")
    listings = driver.instance.find_elements(By.XPATH, "//div[@data-card-type='product']")
    for _ in range(3):
        for listing in listings:
            try:
                if element_exists(listing, By.CLASS_NAME, "anglers-choice-award-badge", time_to_wait=20):
                    click(listing, By.TAG_NAME, 'a')
                    return
            except StaleElementReferenceException:
                listings = driver.instance.find_elements(By.XPATH, "//div[@data-card-type='product']")
                continue


