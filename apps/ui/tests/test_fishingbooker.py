import allure
import pytest
from flaky import flaky
from ..pages.homepage import login_as_an_angler, select_destination_date_and_number_of_persons
from ..pages.charters_search_page import select_angler_requirements, click_first_anglers_choice_listing
from ..pages.charter_view import select_available_date_for_package_and_message_captain


@allure.title('FishingBooker Task for QA')
@allure.description(
    'This is a test task for QA engineer where angler is logging in to the app, visits search results page, '
    'clicks on first available Angler Choice captain and send a message per requested requirements')
@pytest.mark.task
@flaky(max_runs=2, min_passes=1)
def test_fishingbooker_task(setup):
    login_as_an_angler()
    select_destination_date_and_number_of_persons()
    select_angler_requirements()
    click_first_anglers_choice_listing()
    select_available_date_for_package_and_message_captain()



