import requests

import urls
from data import Data
from requests import Response, Request
class Upload:


    @staticmethod
    def upload(task_id: str) -> Response:
        url = f"{urls.BASE_URL_DEV} + {task_id} + {urls.UPLOAD}"
        response = requests.post(
            url,

        )
    @staticmethod
    def upload_ural():
        pass