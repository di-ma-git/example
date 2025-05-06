import requests

import urls
from data import Data
from requests import Response, Request, Session


class CamundaAPI:

    @staticmethod
    def get_instance_id_by_business_key(task_id: str) -> str:
        url = f"{urls.CAMUNDA_URL_DEV}process-instance"
        response = requests.get(
            url,
            params={"businessKey": f"{task_id}"},
            verify=False
        )
        print(f"Camunda response: {response.text}")
        response.raise_for_status()
        return response.json()[0].get("id")

    @staticmethod
    def get_activity_by_instance_id(instance_id: str) -> str:
        url = f"{urls.CAMUNDA_URL_DEV}process-instance/{instance_id}/activity-instances"
        response = requests.get(
            url,
            verify=False
        )
        print(f"Camunda response: {response.text}")
        response.raise_for_status()
        return response.json().get("childActivityInstances")[0].get("childActivityInstances")[0].get("activityId")

    @staticmethod
    def get_history(instance_id: str) -> Response:
        url = f"{urls.CAMUNDA_URL_DEV}history/process-instance/{instance_id}"
        response = requests.get(
            url,
            verify=False
        )
        print(f"Camunda response: {response.text}")
        response.raise_for_status()
        return response

