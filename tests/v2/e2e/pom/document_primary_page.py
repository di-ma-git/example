from http import HTTPStatus

from requests import Session, Response
from common_api.base_api import BaseAPI


class DocumentPrimaryPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session):
        super().__init__(session)

    def get_nationality(self, nationality: str) -> Response:
        params = {"fields[]": ["nationality"]}
        response = self.get(
            "contract",
            params
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents", {}).get("nationality", {}).get("value") == nationality
        return response

    def get_document_primary(self) -> Response:
        response = self.get(
            "contract/uniform/document-primary"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents", {}).get("document")
        self._response = response.json()
        return response

    def next(self, view: str) -> Response:
        contents = self._response.get("contents")
        payload = {
            "data": {
                "document": {
                    "type": contents.get("document", {}).get("type"),
                    "affiliation": contents.get("document", {}).get("affiliation"),
                    "fullName": contents.get("document", {}).get("fullName"),
                    "series": contents.get("document", {}).get("series"),
                    "number": contents.get("document", {}).get("number"),
                    "departmentCode": contents.get("document", {}).get("departmentCode"),
                    "placeOfIssue": contents.get("document", {}).get("placeOfIssue"),
                    "dateOfIssue": contents.get("document", {}).get("dateOfIssue"),
                    "expirationDate": contents.get("document", {}).get("expirationDate"),
                    "dateOfBirth": contents.get("document", {}).get("dateOfBirth"),
                    "placeOfBirth": contents.get("document", {}).get("placeOfBirth"),
                    "readOnly": contents.get("document", {}).get("readOnly"),
                }
            },
            "from": view
        }
        response = self.post(
            "contract/uniform/document-primary/next",
            payload=payload

        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return response
