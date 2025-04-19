import requests

import urls
from data import Data
from requests import Response, Request, Session


class CamundaAPI:

    @staticmethod
    def get_instance_id_by_business_key(task_id: str) -> str:
        response = requests.get(
            f"{urls.CAMUNDA_URL_DEV}",
            params={"businessKey": f"{task_id}"},
            verify=False
        )
        response.raise_for_status()
        return response.json()[0].get("id")

    @staticmethod
    def get_activity_by_instance_id(instance_id: str) -> str:
        response = requests.get(
            f"{urls.CAMUNDA_URL_DEV}/{instance_id}/activity-instances",
            verify=False
        )
        response.raise_for_status()
        return response.json().get("childActivityInstances")[0].get("childActivityInstances")[0].get("activityId")
