import json

import pytest

from common_api.camunda_api import CamundaAPI
from data import Data
from http import HTTPStatus
import helper
from common_api.create import Create
import logging
from context import TestContext
import allure
from allure import attachment_type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def prepare_test_data_fvno(source_value, type_task, provider_value, task_repository, test_context) -> TestContext:
    data = helper.ChangeTestDataHelper.modify_payload_fvno(Data.data_contract_fvno, source_value,
                                                           type_task, provider_value)
    allure.attach(json.dumps(data, indent=4, ensure_ascii=False), name="create", attachment_type=attachment_type.JSON)
    create_response = Create.create_for_e2e_v2(data)
    assert create_response.status_code == HTTPStatus.CREATED

    test_context.set_param("task_id", create_response.json().get("taskId"))
    # TODO переделать на запросы из базы если нужно (возможно будет менее стабильно)
    test_context.set_param("source_value", data['data']['source'])
    test_context.set_param("identification_value", data['data']['identificationValue'])
    test_context.set_param("nationality", data['data']['content']['client'][
        'nationality'])  # можно взять из БД, тк при отсутствии национальности в Create, в БД записывается "RUS"
    test_context.set_param("installer_code", data['data']['content']['contract']['installerCode'])
    instance_id = CamundaAPI.get_instance_id_by_business_key(test_context.get_param("task_id"))
    test_context.set_param("instance_id", instance_id)

    logger.info(f"Task {test_context.get_param("task_id")} created successfully")

    return test_context
