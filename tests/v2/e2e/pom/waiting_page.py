from requests import Session
from common_api.base_api import BaseAPI


class WaitingPage(BaseAPI):
    _response: dict

    def __init__(self, session: Session):
        super().__init__(session)


