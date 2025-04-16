from http import HTTPStatus
import json
from tests.v2.pom.base_api import BaseAPI
from requests import Response, Session


class ClientPage(BaseAPI):
    _response: Response

    def __init__(self, session: Session):
        super().__init__(session)

    def get_client_fields(self) -> Response:
        params = {
            "fields[]": [
                "codeWord",
                "consentToSmsInform",
                "email",
                "inn",
                "middleName",
                "name",
                "nationality",
                "phone",
                "sex",
                "snils",
                "surname"
            ]
        }
        self._response = self.get(
            "contract",
            params
        )
        assert self._response.status_code == HTTPStatus.OK
        assert self._response.json().get("contents")
        return self._response

    def next(self, view: str) -> Response:
        payload = {
            "data": {
                "codeWord": f"{self._response.json().get("contents", {}).get("codeWord", {}).get("value")}",
                "consentToSmsInform": f"{self._response.json().get("contents", {}).get("consentToSmsInform", {}).get("value")}",
                "email": f"{self._response.json().get("contents", {}).get("email", {}).get("value")}",
                "inn": f"{self._response.json().get("contents", {}).get("inn", {}).get("value")}",
                "middleName": f"{self._response.json().get("contents", {}).get("middleName", {}).get("value")}",
                "name": f"{self._response.json().get("contents", {}).get("name", {}).get("value")}",
                "nationality": f"{self._response.json().get("contents", {}).get("nationality", {}).get("value")}",
                "phone": f"{self._response.json().get("contents", {}).get("phone", {}).get("value")}",
                "sex": f"{self._response.json().get("contents", {}).get("sex", {}).get("value")}",
                "snils": f"{self._response.json().get("contents", {}).get("snils", {}).get("value")}",
                "surname": f"{self._response.json().get("contents", {}).get("surname", {}).get("value")}"
            },
            "from": f"{view}"
        }
        response = self.post(
            "contract/fvno/client/next",
            payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return response
