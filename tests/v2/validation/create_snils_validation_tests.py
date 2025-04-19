import urls
from data import MultipartFormData
from data import Data
from data import Data_doc
import requests
import pytest
import helper
from common_api.create import Create
from http import HTTPStatus
from jsonschema import validate
import allure


class TestCreateSnilsValidation:
    # source_value = ['CRM_VOLGA_V2']
    source_value = ['CRM_VOLGA_V2', 'CRM_URAL_V2', 'CRM_FAR_EAST_V2']
    type_task = ['CONTRACT_FVNO']

    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    @pytest.mark.parametrize('snils', [
        "123-456-789 12",
        "000-000-000 00",
        "111-235-434 99",
        None
        # отсутствует

    ])
    def test_create_success_snils_validation(self, task_repository, create_success_schema, source_value, type_task,
                                             snils):
        with allure.step("Prepare test data for request"):
            data = helper.ChangeTestDataHelper.modify_payload_body_for_client_validation(Data.data_contract_fvno,
                                                                                         source_value, type_task,
                                                                                         'snils', snils)

        with allure.step("Send request and check status"):
            response = Create.create(data)
            assert response.status_code == HTTPStatus.CREATED and response.json() is not None

        with allure.step("Check json schema"):
            validate(instance=response.json(), schema=create_success_schema)

        with allure.step("Check write data in database"):
            data = task_repository.get_task_by_task_id(response.json()['taskId'])
            assert data["content"]["client"]["snils"] == snils

        with allure.step("Clean test data from database"):
            task_repository.delete_task_by_task_id_from_all_tables(response.json()['taskId'])

    source_value = ['CRM_VOLGA_V2']
    # source_value = ['CRM_VOLGA_V2', 'CRM_URAL_V2', 'CRM_FAR_EAST_V2']
    type_task = ['CONTRACT_FVNO']

    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    @pytest.mark.parametrize('snils', [
        "23-456-789 12",
        "123_456_789 12",
        "987-654-321-12",
        "ААА-БББ-ВВВ-ГГ",
        "ААА-БББ-ВВВ ГГ",
        "987-654-321-123",
        "987-654-321 123",
        "12345678901",
        "1234567890123",
        "12345678901a",
        "123 456 789 12",
        "строка",
        "",
        " "
    ])
    def test_create_failed_snils_validation(self, task_repository, create_error_schema, source_value, type_task,
                                            snils):
        with allure.step("Prepare test data for request"):
            data = helper.ChangeTestDataHelper.modify_payload_body_for_client_validation(Data.data_contract_fvno,
                                                                                         source_value, type_task,
                                                                                         'snils', snils)
        with allure.step("Send request and check status"):
            response = Create.create(data)
            assert response.status_code == HTTPStatus.BAD_REQUEST

        with allure.step("Check json schema"):
            validate(instance=response.json(), schema=create_error_schema)

    source_value = ['CRM_VOLGA_V2', 'CRM_URAL_V2', 'CRM_FAR_EAST_V2']
    # source_value = ['CRM_VOLGA_V2']
    type_task = ['CONTRACT_FVNO']

    @pytest.mark.validation
    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    @pytest.mark.parametrize('snils', [
        {"data.content.client.snils": "123-456-789 12"},
        {"data.content.client.snils": "000-000-000 00"},
        {"data.content.client.snils": "111-235-434 99"},
        {"data.content.client.snils": None},
        {"data.content.client.snils": "отсутствует"}  # параметр отсутствует
    ])
    def test_create_success_snils_validation(self, task_repository, create_success_schema, source_value, type_task,
                                             snils):
        with allure.step("Prepare test data for request"):
            data = helper.ChangeTestDataHelper.modify_payload_body_for_validation(Data.data_contract_fvno,
                                                                                  source_value, type_task,
                                                                                  snils)

        with allure.step("Send request and check status"):
            response = Create.create(data)
            assert response.status_code == HTTPStatus.CREATED and response.json() is not None

        with allure.step("Check json schema"):
            validate(instance=response.json(), schema=create_success_schema)

        with allure.step("Check write data in database"):
            task_data = task_repository.get_task_by_task_id(response.json()['taskId'])
            if snils["data.content.client.snils"] == "отсутствует":
                assert task_data["content"]["client"]["snils"] is None
            else:
                assert task_data["content"]["client"]["snils"] == snils["data.content.client.snils"]

        with allure.step("Clean test data from database"):
            task_repository.delete_task_by_task_id_from_all_tables(response.json()['taskId'])

    # source_value = ['CRM_VOLGA_V2']
    source_value = ['CRM_VOLGA_V2', 'CRM_URAL_V2', 'CRM_FAR_EAST_V2']
    type_task = ['CONTRACT_FVNO']

    @pytest.mark.validation
    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    @pytest.mark.parametrize('snils', [
        {"data.content.client.snils": "23-456-789 12"},
        {"data.content.client.snils": "123_456_789 12"},
        {"data.content.client.snils": "987-654-321-12"},
        {"data.content.client.snils": "ААА-БББ-ВВВ-ГГ"},
        {"data.content.client.snils": "ААА-БББ-ВВВ ГГ"},
        {"data.content.client.snils": "987-654-321-123"},
        {"data.content.client.snils": "987-654-321 123"},
        {"data.content.client.snils": "12345678901"},
        {"data.content.client.snils": "1234567890123"},
        {"data.content.client.snils": "12345678901a"},
        {"data.content.client.snils": "123 456 789 12"},
        {"data.content.client.snils": "строка"},
        {"data.content.client.snils": ""},
        {"data.content.client.snils": " "}
    ])
    def test_create_failed_snils_validation(self, task_repository, create_error_schema, source_value, type_task,
                                            snils):
        with allure.step("Prepare test data for request"):
            data = helper.ChangeTestDataHelper.modify_payload_body_for_validation(Data.data_contract_fvno,
                                                                                  source_value, type_task, snils)
        with allure.step("Send request and check status"):
            response = Create.create(data)
            assert response.status_code == HTTPStatus.BAD_REQUEST

        with allure.step("Check json schema"):
            validate(instance=response.json(), schema=create_error_schema)
