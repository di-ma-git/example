import urls
from data import MultipartFormData
from data import Data
from data import Data_doc
import requests
import pytest
import helper
from api.create import Create
from http import HTTPStatus
from jsonschema import validate
import allure


class TestCreateValidation:
    source_value = ['CRM_VOLGA_V3']
    # source_value = ['CRM_VOLGA_V3', 'CRM_URAL_V3', 'CRM_FAR_EAST_V3']
    type_task = ['CONVERGENT_SELF']

    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    @pytest.mark.parametrize('email', [
        "maltsev.d@rt.ru",
        "user.name@example.com",
        "1user.name@example.com",
        "ui@example.com",
        "user-123@example-domain.com",
        "user_name.2023@test.co",
        "data.science@domain-expert.org",
        "user.name@22.com",
        "user.name@t2.com",
        "user.name@t_2.com",
        "user.name@t-2.com",
        "user.name@t-2.commm",
        "exampleexampleexampleexampleexampleexampleexamplee@example.com",
        "user.name@exampleexampleexampleexampleexampleexampleexample.com"
    ])
    def test_create_success_email_validation(self, task_repository, create_success_schema, source_value, type_task, email):
        with allure.step("Prepare test data for request"):
            data = helper.ChangeTestDataHelper.modify_payload_body_for_validation(Data.data_convergent_self_v3, source_value, type_task, email)

        with allure.step("Send request and check status"):
            response = Create.create_and_cancel_v3(data)
            assert response.status_code == HTTPStatus.CREATED and response.json() is not None

        with allure.step("Check json schema"):
            validate(instance=response.json(), schema=create_success_schema)

        with allure.step("Check write data in database"):
            data = task_repository.get_task_by_task_id(response.json()['taskId'])
            assert data["content"]["client"]["email"] == email

        with allure.step("Clean test data from database"):
            task_repository.delete_task_by_task_id_from_all_tables(response.json()['taskId'])



    source_value = ['CRM_VOLGA_V3']
    # source_value = ['CRM_VOLGA_V3', 'CRM_URAL_V3', 'CRM_FAR_EAST_V3']
    type_task = ['CONVERGENT_SELF']

    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    @pytest.mark.parametrize('email', [
        "user.name@exampleexampleexampleexampleexampleexampleexampleex.com",
        "user.name@t--2.com",
        "user.name@t__2.com",
        "user.name@t-2.commmm",
        "user.name@t-2.c",
        "exampleexampleexampleexampleexampleexampleexampleex@example.com",
        "@example.com",
        "4124@example.com",
        "u@example.com",
        "u@example.com",
        "0@example.com",
        "data.science@domain-expert.org",
        "_tttt0@example.com",
        "tttt0-@example.com",
        "мальцев@example.com",
        "user--name@example.com",
        "user__name@example.com",
        "мальцев@example.com",
        "мальцев@example.com",
        "мальцев@example.com",
        ".username@example.com",
        "user-name-@example.com",
        "user..name@example.com",
        "user.name@example.com1",
        "user.name@example.com1",
        "user.name@2.com",
        ""
    ])
    def test_create_failed_email_validation(self, task_repository, create_error_schema, source_value, type_task, email):
        with allure.step("Prepare test data for request"):
            data = helper.ChangeTestDataHelper.modify_payload_body_for_validation(Data.data_convergent_self_v3, source_value, type_task, email)

        with allure.step("Send request and check status"):
            response = Create.create_and_cancel_v3(data)
            assert response.status_code == HTTPStatus.BAD_REQUEST

        with allure.step("Check json schema"):
            validate(instance=response.json(), schema=create_error_schema)
