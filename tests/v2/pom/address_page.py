from http import HTTPStatus

from requests import Session, Response
from tests.v2.pom.base_api import BaseAPI


class AddressPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session):
        super().__init__(session)

    def get_addresses(self) -> Response:
        params = {
            "fields[]": [
                "installationAddressFlat",
                "installationAddressGlobalId",
                "installationAddressHouse",
                "installationAddressManual",
                "installationAddressRegion",
                "installationAddressStreet",
                "installationAddressSuggestions",
                "installationAddressTown",
                "installationAddressZipCode",
                "nationality",
                "registrationAddressFlat",
                "registrationAddressGlobalId",
                "registrationAddressHouse",
                "registrationAddressManual",
                "registrationAddressRegion",
                "registrationAddressStreet",
                "registrationAddressSuggestions",
                "registrationAddressTown",
                "registrationAddressZipCode"
            ]
        }
        response = self.get(
            "contract",
            params=params
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        self._response = response.json()
        return response

    def next(self, view: str) -> Response:
        contents = self._response.get("contents", {})
        payload = {
            "data": {
                "registrationAddressFlat": contents.get("registrationAddressFlat", {}).get("value"),
                "registrationAddressGlobalId": contents.get("registrationAddressGlobalId", {}).get("value"),
                "registrationAddressHouse": contents.get("registrationAddressHouse", {}).get("value"),
                "registrationAddressManual": contents.get("registrationAddressManual", {}).get("value"),
                "registrationAddressRegion": contents.get("registrationAddressRegion", {}).get("value"),
                "registrationAddressStreet": contents.get("registrationAddressStreet", {}).get("value"),
                "registrationAddressSuggestions": contents.get("registrationAddressSuggestions", {}).get("value"),
                "registrationAddressTown": contents.get("registrationAddressTown", {}).get("value"),
                "registrationAddressZipCode": contents.get("registrationAddressZipCode", {}).get("value")
            },
            "from": view
        }
        response = self.post(
            "contract/fvno/address/next",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return response
