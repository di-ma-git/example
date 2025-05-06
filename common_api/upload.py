import requests
import urls
from data import Data
from requests import Response, Request
from models.upload import upload_ural, upload


class Upload:

    @staticmethod
    def upload(task_id: str) -> Response:
        url = f"{urls.BASE_URL_DEV}{urls.CREATE_TASK}{task_id}{urls.UPLOAD}"
        response = requests.post(
            url,
            headers=Data.headers2,
            json=upload,
            verify=False
        )
        print(f"Upload response: {response.text}")
        response.raise_for_status()
        return response

    @staticmethod
    def upload_ural(task_id: str) -> Response:
        url = f"{urls.BASE_URL_DEV}{urls.CREATE_TASK}{task_id}{urls.UPLOAD}"
        response = requests.post(
            url,
            headers=Data.headers2,
            json=upload_ural,
            verify=False
        )
        print(f"Upload response: {response.text}")
        response.raise_for_status()
        return response

    @staticmethod
    def upload_common(task_id: str, source: str) -> Response:
        url = f"{urls.BASE_URL_DEV}{urls.CREATE_TASK}{task_id}{urls.UPLOAD}"
        if source == "CRM_URAL_V2":
            response = requests.post(
                url,
                headers=Data.headers2,
                json=upload_ural,
                verify=False
            )
            print(f"Upload response: {response.text}")
            response.raise_for_status()
            return response
        else:
            response = requests.post(
                url,
                headers=Data.headers2,
                json=upload,
                verify=False
            )
            print(f"Upload response: {response.text}")
            response.raise_for_status()
            return response
