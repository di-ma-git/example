import requests

import urls
from data import Data
from requests import Response, Request


class Upload:

    @staticmethod
    def upload(task_id: str) -> Response:
        url = f"{urls.BASE_URL_DEV}{urls.CREATE_TASK}{task_id}{urls.UPLOAD}"
        response = requests.post(
            url,
            headers=Data.headers2,
            json=Data.data_upload_file_links,
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
            json=Data.data_upload_file_links_ural,
            verify=False
        )
        print(f"Upload response: {response.text}")
        response.raise_for_status()
        return response


    @staticmethod
    def common_upload(task_id: str, source: str) -> Response:
        if source == "CRM_URAL_V2":
            url = f"{urls.BASE_URL_DEV}{urls.CREATE_TASK}{task_id}{urls.UPLOAD}"
            response = requests.post(
                url,
                headers=Data.headers2,
                json=Data.data_upload_file_links_ural,
                verify=False
            )
            print(f"Upload response: {response.text}")
            response.raise_for_status()
            return response
        else:
            url = f"{urls.BASE_URL_DEV}{urls.CREATE_TASK}{task_id}{urls.UPLOAD}"
            response = requests.post(
                url,
                headers=Data.headers2,
                json=Data.data_upload_file_links,
                verify=False
            )
            print(f"Upload response: {response.text}")
            response.raise_for_status()
            return response
