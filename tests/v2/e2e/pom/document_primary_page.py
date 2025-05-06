from http import HTTPStatus

from requests import Session, Response
from common_api.base_api import BaseAPI
from context import TestContext


class DocumentPrimaryPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session, test_context: TestContext):
        super().__init__(session)
        self._test_context = test_context

    def get_nationality(self) -> 'DocumentPrimaryPage':
        params = {"fields[]": ["nationality"]}
        response = self.get(
            "contract",
            params
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents", {}).get("nationality", {}).get("value") == self._test_context.get_param(
            "nationality")
        return self

    def get_document_primary(self) -> 'DocumentPrimaryPage':
        response = self.get(
            "contract/uniform/document-primary"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("contents", {}).get("document")
        self._response = response.json()
        return self

    def next(self) -> 'DocumentPrimaryPage':
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
            "from": self._test_context.get_param("current_view")
        }
        response = self.post(
            "contract/uniform/document-primary/next",
            payload=payload

        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get("status") == "success"
        return self
