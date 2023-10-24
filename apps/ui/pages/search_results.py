from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from ..core import driver
from ..utilities.elements import click, wait, element_exists

# Locators
INSHORE_FISHING_LOCATOR = (By.XPATH, '//label[@for="fishing_type_inshore"]')
RED_SNAPPER_LOCATOR = (By.XPATH, '//label[@for="snapper_red"]')
REVIEW_SCORE_LOCATOR = (By.XPATH, '//label[@for="4_50"]')
ANGLERS_CHOICE_LISTING_LOCATOR = (By.XPATH, "//div[@data-card-type='product']")
ANGLERS_CHOICE_BADGE_LOCATOR = (By.CLASS_NAME, "anglers-choice-award-badge")
CHARTER_LIST_CONTAINER_LOCATOR = (By.ID, "charter-list-container")


def select_inshore_fishing():
    click(driver.instance, *INSHORE_FISHING_LOCATOR)


def select_red_snapper():
    click(driver.instance, *RED_SNAPPER_LOCATOR)


def select_review_score():
    click(driver.instance, *REVIEW_SCORE_LOCATOR)


def select_angler_requirements():
    select_red_snapper()
    select_review_score()
    select_inshore_fishing()


def click_first_anglers_choice_listing():
    wait(driver.instance, *CHARTER_LIST_CONTAINER_LOCATOR)
    listings = driver.instance.find_elements(*ANGLERS_CHOICE_LISTING_LOCATOR)
    for _ in range(3):
        for listing in listings:
            try:
                if element_exists(listing, *ANGLERS_CHOICE_BADGE_LOCATOR, time_to_wait=20):
                    click(listing, By.TAG_NAME, 'a')
                    return
            except StaleElementReferenceException:
                listings = driver.instance.find_elements(*ANGLERS_CHOICE_LISTING_LOCATOR)
                continue
