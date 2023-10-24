import pytest
import allure
from flaky import flaky
from .api import Api
import os
import json


@pytest.fixture
def setup():
    device_id = '52E7614C-4C4C-4450-A3D5-AE6F7E550B43'
    application = 'captain|1.5.4'
    device = 'iPhone 11 Pro Max|iOS|13.1'
    token = 'gyY4sBqmr8cXqYgvY6g3'
    return Api(device_id, application, device, token)


@pytest.fixture
def cleanup_photos(setup):
    crew_member_id = '849'
    path = f'/crew_member_photos?crew_member_id={crew_member_id}'
    response = setup.request(path=path, method='GET')
    if response['status_code'] == 200:
        photo_data = json.loads(response['content'].decode('utf-8'))['data']
        if 'id' in photo_data:
            photo_id = photo_data['id']
            delete_path = f'/crew_member_photos/{photo_id}'
            setup.request(path=delete_path, method='DELETE')
        else:
            print("No photo ID found in the response")
    else:
        print(f"Failed to fetch photos. Status code: {response['status_code']}")


@pytest.fixture
def photo_id(setup, cleanup_photos):
    path = '/crew_member_photos'
    data = {'crew_member_id': '849'}
    with open('apps/api/images/image.jpeg', 'rb') as photo_file:
        files = {'photo': ('image.jpeg', photo_file, 'image/jpeg')}
        response = setup.request(path=path, method='POST', files=files, data=data)
    if response['status_code'] == 200:  # Updated status code
        content = json.loads(response['content'].decode('utf-8'))
        return content['data']['id']
    else:
        pytest.fail(f"Photo creation failed: {response}")


@allure.feature('Crew Member Photos API')
class TestCrewMemberPhotos:
    crew_member_id_get = 848
    crew_member_id_post = 849
    invalid_crew_member_id = 999
    valid_photo_path = 'apps/api/images/image.jpeg'
    invalid_photo_path = 'apps/api/images/invalid_image.txt'

    @allure.title('Get Crew Member Photos - Positive')
    @allure.description('Test to verify getting crew member photos with valid crew_member_id')
    @pytest.mark.positive
    @flaky(max_runs=3, min_passes=1)
    def test_get_crew_member_photos_positive(self, setup):
        path = f'/crew_member_photos?crew_member_id={self.crew_member_id_get}'
        response = setup.request(path=path, method='GET')
        assert response['status_code'] == 200

    @allure.title('Create Crew Member Photo - Positive')
    @allure.description('Test to verify creating a crew member photo with valid data')
    @pytest.mark.positive
    def test_create_crew_member_photos_positive(self, setup):
        path = '/crew_member_photos'
        with open(self.valid_photo_path, 'rb') as photo_file:
            files = {'photo': ('image.jpeg', photo_file, 'image/jpeg')}
            data = {'crew_member_id': self.crew_member_id_post}
            response = setup.request(path=path, method='POST', files=files, data=data)
        if response['status_code'] == 422:
            assert "Crew member has a photo already." in response['content'].decode('utf-8')
        else:
            assert response['status_code'] == 200, "Expected a 200 OK status code for successful creation"

    @allure.title('Update Crew Member Photo - Positive')
    @allure.description('Test to verify updating a crew member photo with valid data')
    @pytest.mark.positive
    def test_update_crew_member_photos_positive(self, setup, photo_id):
        path = f'/crew_member_photos/{photo_id}'
        with open('apps/api/images/image1.jpeg', 'rb') as photo_file:
            files = {'photo': ('image1.jpeg', photo_file, 'image/jpeg')}
            data = {'_method': 'patch'}
            response = setup.request(path=path, method='POST', files=files, data=data)
        assert response['status_code'] == 200, "Expected a 200 OK status code for successful update"

    @allure.title('Delete Crew Member Photo - Positive')
    @allure.description('Test to verify deleting a crew member photo with valid data')
    @pytest.mark.positive
    def test_delete_crew_member_photos_positive(self, setup, photo_id):
        path = f'/crew_member_photos/{photo_id}'
        response = setup.request(path=path, method='DELETE')
        assert response['status_code'] == 204, "Expected a 204 No Content status code for successful deletion"

    @allure.title('Get Crew Member Photos - Negative')
    @allure.description('Test to verify getting crew member photos with invalid crew_member_id')
    @pytest.mark.negative
    def test_get_crew_member_photos_negative(self, setup):
        path = f'/crew_member_photos?crew_member_id={self.invalid_crew_member_id}'
        response = setup.request(path=path, method='GET')
        assert response['status_code'] == 404, "Expected a 404 Not Found status code for invalid crew_member_id"

    @allure.title('Create Crew Member Photo - Negative')
    @allure.description('Test to verify creating a crew member photo with invalid data')
    @pytest.mark.negative
    def test_create_crew_member_photos_negative(self, setup):
        path = '/crew_member_photos'
        with open(self.invalid_photo_path, 'rb') as photo_file:
            files = {'photo': ('invalid_image.txt', photo_file, 'text/plain')}
            data = {'crew_member_id': self.crew_member_id_post}
            response = setup.request(path=path, method='POST', files=files, data=data)
        assert response['status_code'] == 422, "Expected a 422 Unprocessable Entity status code for invalid photo data"

    @allure.title('Update Crew Member Photo - Negative')
    @allure.description('Test to verify updating a crew member photo with invalid data')
    @pytest.mark.negative
    def test_update_crew_member_photos_negative(self, setup, photo_id):
        path = f'/crew_member_photos/{photo_id}'
        with open(self.invalid_photo_path, 'rb') as photo_file:
            files = {'photo': ('invalid_image.txt', photo_file, 'text/plain')}
            data = {'_method': 'patch'}
            response = setup.request(path=path, method='POST', files=files, data=data)
        assert response['status_code'] == 422, "Expected a 422 Unprocessable Entity status code for invalid update data"

    @allure.title('Delete Crew Member Photo - Negative')
    @allure.description('Test to verify deleting a crew member photo with invalid photo_id')
    @pytest.mark.negative
    def test_delete_crew_member_photos_negative(self, setup):
        path = '/crew_member_photos/999'
        response = setup.request(path=path, method='DELETE')
        assert response['status_code'] == 404, "Expected a 404 Not Found status code for invalid photo_id"
