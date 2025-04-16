from http import HTTPStatus

from requests import Session, Response
from tests.v2.pom.base_api import BaseAPI


class WaitingPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session):
        super().__init__(session)


