import pytest
import requests
from common_api.create import Create
# from common_api.provide import Provide
from data import Data
import helper
from http import HTTPStatus
from jsonschema import validate
import allure
import json
import urls
import time
from requests import Session
from tests.v2.pom.base_api import BaseAPI
from tests.v2.pom.register_page import RegisterPage
from tests.v2.pom.login_page import LoginPage
from tests.v2.pom.offer_page import OfferPage
from tests.v2.pom.client_page import ClientPage
from tests.v2.pom.email_confirm_page import EmailConfirmPage
from tests.v2.pom.document_primary_page import DocumentPrimaryPage
from tests.v2.pom.address_page import AddressPage
from tests.v2.pom.equipment_page import EquipmentPage
from tests.v2.pom.waiting_page import WaitingPage
from tests.v2.pom.pdf_preview_page import PdfPreviewPage
from tests.v2.pom.employee_confirm_page import EmployeeConfirmPage
from tests.v2.pom.client_signature_page import ClientSignature
from common_api.upload import Upload


class TestE2EContractFvno:
    _task_id: str
    _identificationValue: str
    _current_view: str
    _nationality: str
    _installer_code: str

    # source_value = ['CRM_VOLGA_V2', 'CRM_SOUTH_V2', 'CRM_NORTH_WEST_V2' 'CRM_URAL_V2',
    #                 'CRM_FAR_EAST_V2']
    source_value = ['CRM_URAL_V2']
    type_task = ['CONTRACT_FVNO']
    provider_value = ['TINKOFF']

    # provider_value = ['TINKOFF', 'MTS']

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.base_api = BaseAPI(session)
        self.register_page = RegisterPage(session)
        self.login_page = LoginPage(session)
        self.offer_page = OfferPage(session)
        self.client_page = ClientPage(session)
        self.email_confirm_page = EmailConfirmPage(session)
        self.document_primary_page = DocumentPrimaryPage(session)
        self.address_page = AddressPage(session)
        self.equipment_page = EquipmentPage(session)
        self.waiting_page = WaitingPage(session)
        self.pdf_preview_page = PdfPreviewPage(session)
        self.employee_confirm_page = EmployeeConfirmPage(session)
        self.client_signature_page = ClientSignature(session)

    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    @pytest.mark.parametrize('provider_value', provider_value)
    def test_e2e_contract_fvno(self, setup, task_repository, source_value, type_task, provider_value):
        data = helper.ChangeTestDataHelper.modify_payload_fvno(Data.data_contract_fvno, source_value,
                                                               type_task, provider_value)

        create_response = Create.create_for_e2e_v2(data)
        assert create_response.status_code == HTTPStatus.CREATED
        self._task_id = create_response.json().get("taskId")
        self._identificationValue = data['data']['identificationValue']
        self._nationality = data['data']['content']['client']['nationality']
        self._installer_code = data['data']['content']['contract']['installerCode']
        time.sleep(1)

        self.register_page.register(self._identificationValue)
        assert task_repository.get_task_status(self._task_id) == "ACTIVE"

        self.login_page.login("111111", self._identificationValue)
        self.login_page.find_task(self._task_id)
        step = self.login_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "FVNOOffer"

        self.offer_page.settings()
        self.offer_page.next(self._current_view)
        step = self.offer_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "FVNOClient"

        self.client_page.get_client_fields()
        self.client_page.next(self._current_view)
        step = self.client_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "FVNOEmailConfirm"

        self.email_confirm_page.get_email()
        self.email_confirm_page.confirm_email()
        time.sleep(1)
        code = task_repository.get_confirm_email_code_by_task_id(self._task_id)
        self.email_confirm_page.next(code, self._current_view)
        step = self.email_confirm_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "UniformDocumentPrimary"

        nationality = self.document_primary_page.get_nationality()
        assert self._nationality == nationality.json().get("contents", {}).get("nationality", {}).get("value")
        self.document_primary_page.get_document_primary()
        self.document_primary_page.next(self._current_view)
        step = self.document_primary_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "FVNOAddress"

        self.address_page.get_addresses()
        self.address_page.next(self._current_view)
        step = self.address_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "FVNOEquipment"

        self.equipment_page.get_equipment()
        self.equipment_page.alternative(self._current_view)
        step = self.equipment_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "FVNOWaiting" # добавить проверку progress

        # UPLOAD
        response_upload = Upload.common_upload(self._task_id, source_value)
        assert response_upload.status_code == HTTPStatus.OK
        assert response_upload.json().get('success') == True
        time.sleep(10)

        step = self.waiting_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "FVNOWaiting"

        self.pdf_preview_page.get_files()
        self.pdf_preview_page.next(self._current_view)
        step = self.document_primary_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "FVNOEmployeeConfirm"

        self.employee_confirm_page.get_client_document()
        self.employee_confirm_page.employee_confirm()
        # TODO на тесте нужно брать код смс подтверждения из базы
        self.employee_confirm_page.next(self._installer_code, self._current_view)
        step = self.employee_confirm_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "FVNOSignature"

        self.client_signature_page.signature()
        self.client_signature_page.next(self._current_view)
        step = self.client_signature_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "FVNOComplete"

        # UPLOAD
        response_upload = Upload.common_upload(self._task_id, source_value)
        assert response_upload.status_code == HTTPStatus.OK
        assert response_upload.json().get('success') == True
        time.sleep(10)

        assert task_repository.get_task_status(self._task_id) == 'COMPLETED'
        task_repository.delete_task_by_task_id_from_all_tables(self._task_id)

        # TODO проверка отсутствия ошибок в логе
        # TODO проверить логи выборочно???
        # TODO проверить токен в камунде??? через базу или через common_api???

    source_value = ['CRM_SIBERIA_V2']
    type_task = ['CONTRACT_FVNO']
    provider_value = ['TINKOFF']

    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    @pytest.mark.parametrize('provider_value', provider_value)
    def test_e2e_contract_fvno_siberia(self, source_value, type_task, provider_value):
        pass
