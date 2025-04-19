from http import HTTPStatus
import json
from common_api.base_api import BaseAPI
from requests import Response, Session


class ClientPage(BaseAPI):
    _response: dict

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
        response = self.get(
            "contract",
            params
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        self._response = response.json()
        return response

    def next(self, view: str) -> Response:
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
            "from": view
        }
        payload_str = json.dumps(payload, ensure_ascii=False)
        response = self.post(
            "contract/fvno/client/next",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return response

