from http import HTTPStatus

import allure
import urls
from data import MultipartFormData
from data import Data
from data import Data_doc
import requests
import pytest
import helper
from common_api.create import Create
from jsonschema import validate


class TestCreate:
    source_value = ['CRM_MOSCOW_V3', 'CRM_CENTER_V3']
    type_task = ['SIGNING_DOCUMENTS_WRAPPER']
    file_type = ['docremotesite', 'remotemvno', 'remotesite', 'remoteSiteAct', 'EFD.App.Equip.Property',
                 'EFD.App.Equip.Rent', 'EFD.App.Services', 'EFD.App.Works', 'EFD.Contract']

    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    @pytest.mark.parametrize('file_type', file_type)
    def test_create_for_all_process(self, task_repository, create_success_schema, source_value, type_task, file_type):
        with allure.step("Prepare test data for request"):
            data = helper.ChangeTestDataHelper.modify_payload_body(Data.data_wrapper, source_value, type_task)
            file_info = helper.ChangeTestDataHelper.modify_payload_body_file_info(Data.file_info_wrapper, file_type)

        with allure.step("Send request and check status"):
            response = Create.create_and_cancel_for_wrapper_v2(data, file_info)

        with allure.step("Check json schema"):
            assert response.status_code == HTTPStatus.CREATED and response.json() is not None
        with allure.step("Check json schema"):
            validate(instance=response.json(), schema=create_success_schema)

        with allure.step("Clean test data from database"):
            task_repository.delete_task_by_task_id_from_all_tables(response.json()['taskId'])
