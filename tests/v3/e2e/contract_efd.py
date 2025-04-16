import pytest
import requests
from api.create import Create
# from api.provide import Provide
from data import Data
import helper
from http import HTTPStatus
from jsonschema import validate
import allure
import json


class TestE2EContractEfd:
    # source_value = ['CRM_VOLGA_V3', 'CRM_SOUTH_V3', 'CRM_SIBERIA_V3', 'CRM_NORTH_WEST_V3' 'CRM_URAL_V3',
    #                 'CRM_FAR_EAST_V3']
    source_value = ['CRM_SOUTH_V3']
    type_task = ['CONTRACT_EFD']

    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    def test_e2e_contract_efd(self, source_value, type_task):
        with allure.step("Prepare test data for request"):
            data = helper.ChangeTestDataHelper.modify_payload_body(Data.data_contract_efd_v3, source_value, type_task)

        with allure.step("Send request and check status"):
            response = Create.create_for_e2e_v3(data)
            assert response.status_code == HTTPStatus.CREATED

        with allure.step("register"):
            payload_register = {"phone": "9013111215"}
            result1 = requests.request(
                "POST",
                "https://devapp.ed.rt.ru/api/v1/register",
                headers=Data.headers_front,
                data=payload_register,
                verify=False
            )
            assert result1.status_code == HTTPStatus.CREATED

        with allure.step("login"):
            payload_login = {"password": "111111", "phone": "9013111215"}
            result2 = requests.request(
                "POST",
                "https://devapp.ed.rt.ru/api/v1/login",
                headers=Data.headers_front,
                data=payload_login,
                verify=False
            )
            assert result2.status_code == HTTPStatus.CREATED
            token = result2.json().get("contents", {}).get("token")
            headers = Data.headers_front
            headers_front_with_auth = headers["Authorization"][f"Bearer {token}"]

        with allure.step("task"):
            payload_task = {"taskId": "41bb57b2-18d0-45f1-b997-adfa275bf7a9"}
            result3 = requests.request(
                "POST",
                "https://devapp.ed.rt.ru/api/v1/login",
                headers=headers_front_with_auth,
                data=payload_task,
                verify=False
            )
            assert result3.status_code == HTTPStatus.CREATED
