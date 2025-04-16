import time
from http import HTTPStatus
import requests
from requests import Response
from tests.v2.pom.base_api import BaseAPI
from database import task_repository
from requests import Session


class RegisterPage(BaseAPI):

    def __init__(self, session: Session):
        super().__init__(session)

    def register(self, phone: str) -> Response:
        payload = {"phone": phone}
        response = self.post("register", payload)
        assert response.status_code == HTTPStatus.OK

        return response
