import requests
from requests import Response
import urls
from models.provide import provide, provide_ural
from data import Data


class Provide:

    @staticmethod
    def provide_common(task_id: str, source: str) -> Response:
        url = f"{urls.BASE_URL_DEV}{urls.PROVIDE}{task_id}"
        if source == "CRM_URAL_V3":
            response = requests.post(
                url,
                headers=Data.headers2,
                json=provide_ural,
                verify=False
            )
            print(f"Provide response: {response.text}")
            response.raise_for_status()
            return response
        else:
            response = requests.post(
                url,
                headers=Data.headers2,
                json=provide,
                verify=False
            )
            print(f"Provide response: {response.text}")
            response.raise_for_status()
            return response
