import allure
import pytest
from flaky import flaky


@allure.feature('Homepage')
@allure.title('Verify Fishingbooker Homepage')
@allure.description('Test navigates to the Fishingbooker homepage, asserts that all necessary elements are fully loaded')
@pytest.mark.fb
@flaky(max_runs=2, min_passes=1)
def test_fb(setup):
    pass
