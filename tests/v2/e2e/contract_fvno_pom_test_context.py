import pytest

from camunda_checker import CamundaChecker
from common_api.base_api import BaseAPI
from models.camunda_activities.fvno import FVNO
from tests.v2.e2e.pom.register_page import RegisterPage
from tests.v2.e2e.pom.login_page import LoginPage
from tests.v2.e2e.pom.offer_page import OfferPage
from tests.v2.e2e.pom.client_page import ClientPage
from tests.v2.e2e.pom.email_confirm_page import EmailConfirmPage
from tests.v2.e2e.pom.document_primary_page import DocumentPrimaryPage
from tests.v2.e2e.pom.address_page import AddressPage
from tests.v2.e2e.pom.equipment_page import EquipmentPage
from tests.v2.e2e.pom.waiting_page import WaitingPage
from tests.v2.e2e.pom.pdf_preview_page import PdfPreviewPage
from tests.v2.e2e.pom.employee_confirm_page import EmployeeConfirmPage
from tests.v2.e2e.pom.client_signature_page import ClientSignaturePage
from tests.v2.e2e.pom.upload_api import UploadAPI
import allure

class TestE2EContractFvno:
    source_value = ['CRM_VOLGA_V2', 'CRM_SOUTH_V2', 'CRM_NORTH_WEST_V2', 'CRM_URAL_V2', 'CRM_FAR_EAST_V2']
    type_task = ['CONTRACT_FVNO']
    provider_value = ['TINKOFF', 'MTS']

    @pytest.fixture(scope="function")
    def setup(self, session, test_context, task_repository):
        self.base_api = BaseAPI(session)
        self.register_page = RegisterPage(session, test_context)
        self.login_page = LoginPage(session, test_context, task_repository)
        self.offer_page = OfferPage(session, test_context)
        self.client_page = ClientPage(session, test_context)
        self.email_confirm_page = EmailConfirmPage(session, test_context, task_repository)
        self.document_primary_page = DocumentPrimaryPage(session, test_context)
        self.address_page = AddressPage(session, test_context)
        self.equipment_page = EquipmentPage(session, test_context)
        self.waiting_page = WaitingPage(session)
        self.pdf_preview_page = PdfPreviewPage(session, test_context)
        self.employee_confirm_page = EmployeeConfirmPage(session, test_context)
        self.client_signature_page = ClientSignaturePage(session, test_context, task_repository)
        self.upload = UploadAPI(test_context)
        self.camunda_checker = CamundaChecker(test_context)

    @pytest.mark.usefixtures("setup")
    # @pytest.mark.usefixtures("cleanup_database") # cleanup task from db after test
    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    @pytest.mark.parametrize('provider_value', provider_value)
    def test_e2e_contract_fvno(self, task_repository, test_context, prepare_test_data_fvno):

        with allure.step("Check status task is ACTIVE"):
            assert task_repository.get_task_status(test_context.get_param("task_id")) == "ACTIVE"
        with allure.step("Login"):
            self.register_page.register()
            self.login_page.login().find_task()
            step_view_response = self.login_page.step()
            test_context.set_param("current_view", step_view_response.json().get("contents", {}).get("view"))
            assert test_context.get_param("current_view") == "FVNOOffer"

        with allure.step("Accept offer"):
            self.offer_page.settings().next()
            step_view_response = self.offer_page.step()
            test_context.set_param("current_view", step_view_response.json().get("contents", {}).get("view"))
            assert test_context.get_param("current_view") == "FVNOClient"

        with allure.step("Client check client data"):
            self.client_page.get_client_fields().next()
            step_view_response = self.client_page.step()
            test_context.set_param("current_view", step_view_response.json().get("contents", {}).get("view"))
            assert test_context.get_param("current_view") == "FVNOEmailConfirm"

        with allure.step("Confirm email"):
            self.email_confirm_page.get_email().confirm_email().next()
            step_view_response = self.email_confirm_page.step()
            test_context.set_param("current_view", step_view_response.json().get("contents", {}).get("view"))
            assert test_context.get_param("current_view") == "UniformDocumentPrimary"

        with allure.step("Client check passport data"):
            self.document_primary_page.get_nationality().get_document_primary().next()
            step_view_response = self.document_primary_page.step()
            test_context.set_param("current_view", step_view_response.json().get("contents", {}).get("view"))
            assert test_context.get_param("current_view") == "FVNOAddress"

        with allure.step("Client check addresses"):
            self.address_page.get_addresses().next()
            step_view_response = self.address_page.step()
            test_context.set_param("current_view", step_view_response.json().get("contents", {}).get("view"))
            assert test_context.get_param("current_view") == "FVNOEquipment"

        with allure.step("Client check transferred equipment"):
            self.equipment_page.get_equipment().alternative()
            step_view_response = self.equipment_page.step()
            test_context.set_param("current_view", step_view_response.json().get("contents", {}).get("view"))
            assert test_context.get_param("current_view") == "FVNOWaiting"

        with allure.step("Send UPLOAD and wait 10 sec"):
            self.upload.send()

        with allure.step("Waiting page"):
            step_view_response = self.waiting_page.step()
            test_context.set_param("current_view", step_view_response.json().get("contents", {}).get("view"))
            assert test_context.get_param("current_view") == "FVNOPdfPreview"

        with allure.step("Show documents preview"):
            self.pdf_preview_page.get_files().next()
            step_view_response = self.document_primary_page.step()
            test_context.set_param("current_view", step_view_response.json().get("contents", {}).get("view"))
            assert test_context.get_param("current_view") == "FVNOEmployeeConfirm"

        with allure.step("Installer confirm client information is correct"):
            self.employee_confirm_page.get_client_document().employee_confirm().next()
            step_view_response = self.employee_confirm_page.step()
            test_context.set_param("current_view", step_view_response.json().get("contents", {}).get("view"))
            assert test_context.get_param("current_view") == "FVNOSignature"

        with allure.step("Client sign documents with sms code"):
            self.client_signature_page.signature().next()
            step_view_response = self.client_signature_page.step()
            test_context.set_param("current_view", step_view_response.json().get("contents", {}).get("view"))
            assert test_context.get_param("current_view") == "FVNOComplete"

        with allure.step("Send UPLOAD and wait 10 sec"):
            self.upload.send()

        with allure.step("Check task status is COMPLETED"):
            assert task_repository.get_task_status(test_context.get_param("task_id")) == 'COMPLETED'

        with allure.step("Check Camunda activities path"):
            assert self.camunda_checker.check_history_activities(FVNO.happy_path_with_preview_activities_ids)
