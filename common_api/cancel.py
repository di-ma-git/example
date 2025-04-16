import urls
from data import MultipartFormData
from data import Data
import requests
import pytest
import helper


class Cancel:
    @staticmethod
    def cancel(taskId):
            url = urls.BASE_URL_DEV + taskId + "/cancel?reason=OK"
            response_cancel = requests.request("POST", url, headers=Data.headers1, verify=False)
            print(response_cancel)
            return response_cancel
