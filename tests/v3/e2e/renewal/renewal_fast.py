import pytest

from common_api.base_api import BaseAPI
import urls
from models.enums_form.renewal import RenewalFormUralV3
from models.enums_form.secondary_documents import SecondaryDocumentsV3
from data import Data
from camunda_checker import CamundaChecker
from tests.v3.e2e.api.provide_api import ProvideAPI
from models.camunda_activities.renewal import RenewalV3


class TestRenewalFast:
    source_value = ['CRM_URAL_V3']
    type_task = ['RENEWAL']

    @pytest.fixture(scope="function")
    def setup(self, session, test_context):
        url = f"{urls.BASE_URL_DEV}{urls.EDOGOVOR}"
        self.base_api = BaseAPI(session, base_url=url, headers=Data.headers1)
        self.provide = ProvideAPI(test_context)
        self.camunda_checker = CamundaChecker(test_context)

    @pytest.mark.usefixtures("setup")
    @pytest.mark.parametrize("source_value", source_value)
    @pytest.mark.parametrize("type_task", type_task)
    def test_renewal_ural_fast(self, test_context, task_repository, prepare_test_data_renewal):
        self.base_api.step_begin(test_context.get_param("task_id"))
        self.base_api.move(test_context.get_param("task_id"), RenewalFormUralV3.URAL_RENEWAL_EFD_OFFER.value)
        self.base_api.move(test_context.get_param("task_id"), RenewalFormUralV3.URAL_RENEWAL_EFD_CLIENT.value)
        self.base_api.move(test_context.get_param("task_id"), RenewalFormUralV3.URAL_RENEWAL_EFD_EMAIL_CONFIRM.value)
        self.base_api.move(test_context.get_param("task_id"), SecondaryDocumentsV3.UNIFORM_DOCUMENT_PRIMARY.value)
        self.base_api.move(test_context.get_param("task_id"), RenewalFormUralV3.URAL_RENEWAL_EFD_ADDRESS.value)
        self.base_api.move(test_context.get_param("task_id"), RenewalFormUralV3.URAL_RENEWAL_EFD_DELEVERY.value)
        self.base_api.move(test_context.get_param("task_id"), RenewalFormUralV3.URAL_RENEWAL_EFD_EMAIL_CONFIRM.value)
        self.base_api.otp_sig("333333", test_context.get_param("task_id"))
        self.base_api.save_form_fields(test_context.get_param("task_id"),
                                       RenewalFormUralV3.URAL_RENEWAL_EFD_SIGNATURE.value)
        self.base_api.move(test_context.get_param("task_id"), RenewalFormUralV3.URAL_RENEWAL_EFD_SIGNATURE.value)
        self.provide.send()

        assert task_repository.get_task_status(test_context.get_param("task_id")) == 'COMPLETED'
        assert self.camunda_checker.check_history_activities(
            RenewalV3.happy_path_without_preview_activities_ids) is True
