import json
from http import HTTPStatus
import random

from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import urls
from data import Data
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LoggingHTTPAdapter(HTTPAdapter):
    def send(self, request, **kwargs):
        attempt = 1
        while True:
            try:
                logger.debug(f"Try {attempt}: Sending request to {request.url}")
                response = super().send(request, **kwargs)
                logger.debug(f"Try {attempt}: Server response {response.status_code}")
                return response
            except Exception as e:
                logger.debug(f"Try {attempt}: error - {e}")
                if attempt >= self.max_retries.total:
                    logger.error("The maximum number of attempts has been reached")
                    raise
                attempt += 1


class BaseAPI:

    def __init__(self, session: Session = None, base_url: str = None, headers: dict = None):
        self.session = session or Session()
        self.base_url = base_url if base_url else urls.BASE_URL_FVNO
        self.headers = headers or Data.headers_front
        self.session.headers.update(self.headers)
        self.session.mount("http://", LoggingHTTPAdapter(max_retries=Retry(total=3, backoff_factor=3)))

    def get(self, path: str, params: dict = None) -> Response:
        logger.info(f"Get request to {path} with params {params}")
        response = self.session.get(
            f"{self.base_url}{path}",
            headers=self.headers,
            params=params,
            verify=False
        )
        logger.info(f"Response: {response}")
        response.raise_for_status()
        return response

    def post(
            self,
            path: str,
            params: dict = None,
            payload: dict = None,
            data: str = None
    ) -> Response:

        if payload is not None:
            logger.info(f"POST request to {path} with payload {payload}")
            response = self.session.post(
                f"{self.base_url}{path}",
                headers=self.headers,
                params=params,
                json=payload,
                verify=False
            )
            logger.info(f"Response: {response}")
            response.raise_for_status()
            return response

        elif data is not None:
            logger.info(f"POST request to {path} with payload {data}")
            response = self.session.post(
                f"{self.base_url}{path}",
                headers=self.headers,
                params=params,
                data=data,
                verify=False
            )
            logger.info(f"Response: {response}")
            response.raise_for_status()
            return response
        else:
            logger.info(f"POST request to {path} without payload")
            response = self.session.post(
                f"{self.base_url}{path}",
                headers=self.headers,
                params=params,
                verify=False
            )
            logger.info(f"Response: {response}")
            response.raise_for_status()
            return response

    def step(self) -> Response:
        response = self.get("step")
        assert response.status_code == HTTPStatus.OK
        response.raise_for_status()
        return response

    def step_begin(self, task_id: str) -> Response:
        response = self.get(
            f"task/{task_id}/step"
        )
        assert response.status_code == HTTPStatus.OK
        response.raise_for_status()
        return response

    def move(self, task_id: str, form_from: str) -> Response:
        params = {"from": form_from}
        response = self.post(
            f"task/{task_id}/step/next",
            params=params
        )
        assert response.status_code == HTTPStatus.OK
        response.raise_for_status()
        return response

    def otp_sig(self, code: str, task_id: str) -> Response:
        payload = {
            "code": code,
            "taskId": task_id
        }
        response = self.post(
            "otp",
            payload=payload
        )
        assert response.status_code == HTTPStatus.OK
        response.raise_for_status()
        return response

    def save_form_fields(self, task_id: str, form_from: str) -> Response:
        params = {"from": form_from}
        data = {
            "ip": {
                "value": ".".join(str(random.randint(0, 254)) for _ in range(4))
            },
            "source": {
                "value": random.choice(["web", "ecm"])
            }
        }
        response = self.post(
            f"task/{task_id}/step/next",
            params=params,
            data=json.dumps(data, ensure_ascii=False)
        )
        assert response.status_code == HTTPStatus.OK
        response.raise_for_status()
        return response
