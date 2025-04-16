from http import HTTPStatus

from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import urls
from data import Data



class BaseAPI:

    def __init__(self, session: Session = None, base_url: str = None, headers: dict = None):
        self.session = session or Session()
        self.base_url = base_url if base_url else urls.BASE_URL_FVNO
        self.headers = headers or Data.headers_front
        self.session.headers.update(self.headers)
        self.session.mount("http://", HTTPAdapter(max_retries=Retry(total=14, backoff_factor=3))) # вернуть тотал = 3

    def get(self, path: str, params: dict = None) -> Response:
        response = self.session.get(
            f"{self.base_url}{path}",
            headers=self.headers,
            params=params,
            verify=False
        )
        response.raise_for_status()
        return response

    def post(self, path: str, payload: dict = None) -> Response:
        response = self.session.post(
            f"{self.base_url}{path}",
            headers=self.headers,
            json=payload,
            verify=False
        )
        response.raise_for_status()
        return response

    def step(self) -> Response:
        response = self.get("step")
        assert response.status_code == HTTPStatus.OK
        return response
