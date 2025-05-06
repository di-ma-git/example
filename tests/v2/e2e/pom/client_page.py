from http import HTTPStatus
import json
from common_api.base_api import BaseAPI
from requests import Response, Session
from context import TestContext

class ClientPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session, test_context: TestContext):
        super().__init__(session)
        self._test_context = test_context

    def get_client_fields(self) -> 'ClientPage':
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
        response = self.get(
            "contract",
            params
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        self._response = response.json()
        return self

    def next(self) -> 'ClientPage':
        contents = self._response.get("contents")

        payload = {
            "data": {
                "codeWord": contents.get("codeWord", {}).get("value"),
                "consentToSmsInform": contents.get("consentToSmsInform", {}).get("value"),
                "email": contents.get("email", {}).get("value"),
                "inn": contents.get("inn", {}).get("value"),
                "middleName": contents.get("middleName", {}).get("value"),
                "name": contents.get("name", {}).get("value"),
                "nationality": contents.get("nationality", {}).get("value"),
                "phone": contents.get("phone", {}).get("value"),
                "sex": contents.get("sex", {}).get("value"),
                "snils": contents.get("snils", {}).get("value"),
                "surname": contents.get("surname", {}).get("value")
            },
            "from": self._test_context.get_param("current_view")
        }
        payload_str = json.dumps(payload, ensure_ascii=False)
        response = self.post(
            "contract/fvno/client/next",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return self

