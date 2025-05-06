import json
import logging
from http import HTTPStatus

import pytest

import helper
from common_api.camunda_api import CamundaAPI
from common_api.create import Create
from data import Data
import allure
from allure import attachment_type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def prepare_test_data_renewal(type_task, source_value, test_context, task_repository):
    data = helper.ChangeTestDataHelper.modify_payload_body(Data.data_renewal_v3, source_value, type_task)
    allure.attach(json.dumps(data, indent=4, ensure_ascii=False), name="create", attachment_type=attachment_type.JSON)
    create_response = Create.create_for_e2e_v3(data)
    assert create_response.status_code == HTTPStatus.CREATED

    test_context.set_param("task_id", create_response.json().get("taskId"))
    test_context.set_param("source_value", data['data']['source'])
    test_context.set_param("identification_value", data['data']['identificationValue'])
    test_context.set_param("installer_code", data['data']['content']['contract']['installerCode'])
    instance_id = CamundaAPI.get_instance_id_by_business_key(test_context.get_param("task_id"))
    test_context.set_param("instance_id", instance_id)

    logger.info(f"Task {test_context.get_param("task_id")} created successfully")

    return test_context
