from http import HTTPStatus

from requests import Session, Response
from tests.v2.pom.base_api import BaseAPI


class PdfPreviewPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session):
        super().__init__(session)

    def get_files(self) -> Response:
        params = {
            "fields[]": [
                "files"
            ]
        }
        response = self.get(
            "contract",
            params=params
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents")
        # TODO добавить проверку ссылок из UPLOAD
        return response

    def next(self, view: str) -> Response:
        payload = {"from": view}
        response = self.post(
            "contract/fvno/pdf-preview/next",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return response
