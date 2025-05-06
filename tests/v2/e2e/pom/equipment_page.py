from http import HTTPStatus

from requests import Session, Response
from common_api.base_api import BaseAPI
from context import TestContext


class EquipmentPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session, test_context: TestContext):
        super().__init__(session)
        self._test_context = test_context

    def get_equipment(self) -> 'EquipmentPage':
        response = self.get(
            "contract/fvno/equipment"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        return self

    def alternative(self) -> 'EquipmentPage':
        payload = {"from": self._test_context.get_param("current_view")}
        response = self.post(
            "contract/fvno/equipment/alternative",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return self

