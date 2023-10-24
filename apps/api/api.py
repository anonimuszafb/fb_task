import requests
from requests.auth import HTTPBasicAuth


class Api:
    def __init__(self, device_id, application, device, token=None):
        self.headers = {
            'X-Device-Id': device_id,
            'X-Application': application,
            'X-Device': device
        }
        self.auth = HTTPBasicAuth('fishingbooker', 'QAFBTest')
        if token:
            self.headers.update({'Token': token})
        self.base_url = 'https://qahiring.dev.fishingbooker.com/api/v1_3'

    def request(self, path=None, method='GET', payload=None, headers=None, files=None, data=None):
        if headers:
            self.headers.update(headers)
        response = requests.request(method, self.base_url + path if path else self.base_url,
                                    json=payload, headers=self.headers, auth=self.auth, allow_redirects=False,
                                    files=files, data=data)
        return {'status_code': response.status_code, 'content': response.content, 'headers': response.headers}
