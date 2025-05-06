import time
from http import HTTPStatus

from common_api.provide import Provide
from context import TestContext


class ProvideAPI:

    def __init__(self, test_context: TestContext):
        self._test_context = test_context

    def send(self):
        response = Provide.provide_common(
            self._test_context.get_param("task_id"),
            self._test_context.get_param("source_value")
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get('success') is True
        time.sleep(10)
