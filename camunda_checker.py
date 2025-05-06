from http import HTTPStatus

from common_api.camunda_api import CamundaAPI
from context import TestContext


class CamundaChecker:

    def __init__(self, test_context: TestContext):
        self._test_context = test_context

    def check_history_activities(self, key_path_activities: list) -> list:
        response = CamundaAPI.get_history(self._test_context.get_param("instance_id"))
        assert response.status_code == HTTPStatus.OK
        actual_activities = [activity.get("activityId") for activity in response.json()]

        assert is_subsequence(actual_activities,
                              key_path_activities) is True, f"Actual token path doesn't match expected path"

        return actual_activities


def is_subsequence(subsequence: list, sequence: list) -> bool:
    it = iter(sequence)
    return all(item in it for item in subsequence)
