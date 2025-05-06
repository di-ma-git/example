import time
from http import HTTPStatus

from common_api.upload import Upload
from context import TestContext
from database.task_repository import TaskRepository


class UploadAPI:

    def __init__(self, test_context: TestContext):
        self._test_context = test_context

    def send(self):
        response = Upload.upload_common(
            self._test_context.get_param("task_id"),
            self._test_context.get_param("source_value")
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get('success') is True
        time.sleep(10)
