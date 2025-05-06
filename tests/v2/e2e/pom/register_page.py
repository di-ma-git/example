from http import HTTPStatus
from requests import Response
from common_api.base_api import BaseAPI
from requests import Session
from common_api.camunda_api import CamundaAPI
from context import TestContext


class RegisterPage(BaseAPI):

    def __init__(self, session: Session, test_context: TestContext):
        super().__init__(session)
        self._test_context = test_context

    def register(self) -> Response:
        payload = {"phone": self._test_context.get_param("identification_value")}
        response = self.post("register", payload)
        assert response.status_code == HTTPStatus.OK

        # сомнения в этой проверке токена из камунды, где ее лучше делать
        # если делать в основном тесте - это еще больше ухудшит читаемость
        # если делать в page object - в каждый page object придется передавать один и тот же параметр instance_id
        # либо как то инжектить словарь _test_params из теста в page object
        assert "Event_0e3beha" == CamundaAPI.get_activity_by_instance_id(self._test_context.get_param("instance_id"))

        return response
