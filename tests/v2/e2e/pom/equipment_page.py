from http import HTTPStatus

from requests import Session, Response
from common_api.base_api import BaseAPI


class EquipmentPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session):
        super().__init__(session)

    def get_equipment(self) -> Response:
        response = self.get(
            "contract/fvno/equipment"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        return response

    def alternative(self, view: str) -> Response:
        payload = {"from": view}
        response = self.post(
            "contract/fvno/equipment/alternative",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return response

    def check_camunda_token(self):

        response = self.get(
            ""
        )
        activity_id = (response.json().get("childActivityInstances", {})[0]
                       .get("childActivityInstances", {}))[0].get("activityId")
        assert activity_id == "Gateway_0a1zk4n"
