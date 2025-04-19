import pytest
import requests

import urls
from common_api.create import Create
# from common_api.provide import Provide
from data import Data
import helper
from http import HTTPStatus
import time
from common_api.base_api import BaseAPI
from common_api.camunda_api import CamundaAPI
from common_api.upload import Upload
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
from tests.v2.e2e.pom.client_signature_page import ClientSignature


class TestE2EContractFvno:
    _test_params: dict = {}

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

        # TODO Вынести создание задачи и заполнение мапы в хуки
        self._test_params["task_id"] = create_response.json().get("taskId")
        self._test_params["identification_value"] = data['data']['identificationValue']
        self._test_params["nationality"] = data['data']['content']['client']['nationality']
        self._test_params["installer_code"] = data['data']['content']['contract']['installerCode']
        self._test_params["instance_id"] = CamundaAPI.get_instance_id_by_business_key(self._test_params.get("task_id"))
        time.sleep(1)

        self.register_page.register(self._test_params.get("identification_value"), self._test_params.get("instance_id"))
        assert task_repository.get_task_status(self._test_params.get("task_id")) == "ACTIVE"

        # TODO на Тесте нужно брать сгенерированный код смс подтверждения из БД
        self.login_page.login("111111", self._test_params.get("identification_value"))
        self.login_page.find_task(self._test_params.get("task_id"))
        step = self.login_page.step()
        self._test_params["current_view"] = step.json().get("contents", {}).get("view")
        assert self._test_params.get("current_view") == "FVNOOffer"

        self.offer_page.settings()
        self.offer_page.next(self._test_params.get("current_view"))
        step = self.offer_page.step()
        self._test_params["current_view"] = step.json().get("contents", {}).get("view")
        assert self._test_params.get("current_view") == "FVNOClient"

        self.client_page.get_client_fields()
        self.client_page.next(self._test_params.get("current_view"))
        step = self.client_page.step()
        self._test_params["current_view"] = step.json().get("contents", {}).get("view")
        assert self._test_params.get("current_view") == "FVNOEmailConfirm"

        self.email_confirm_page.get_email()
        self.email_confirm_page.confirm_email()
        time.sleep(3)
        code = task_repository.get_confirm_email_code_by_task_id(self._test_params.get("task_id"))
        self.email_confirm_page.next(code, self._test_params.get("current_view"))
        step = self.email_confirm_page.step()
        self._test_params["current_view"] = step.json().get("contents", {}).get("view")
        assert self._test_params.get("current_view") == "UniformDocumentPrimary"

        self.document_primary_page.get_nationality(self._test_params.get("nationality"))
        self.document_primary_page.get_document_primary()
        self.document_primary_page.next(self._test_params.get("current_view"))
        step = self.document_primary_page.step()
        self._test_params["current_view"] = step.json().get("contents", {}).get("view")
        assert self._test_params.get("current_view") == "FVNOAddress"

        self.address_page.get_addresses()
        self.address_page.next(self._test_params.get("current_view"))
        step = self.address_page.step()
        self._test_params["current_view"] = step.json().get("contents", {}).get("view")
        assert self._test_params.get("current_view") == "FVNOEquipment"

        self.equipment_page.get_equipment()
        self.equipment_page.alternative(self._test_params.get("current_view"))
        step = self.equipment_page.step()
        self._test_params["current_view"] = step.json().get("contents", {}).get("view")
        assert self._test_params.get("current_view") == "FVNOWaiting" # добавить проверку progress

        # UPLOAD
        response_upload = Upload.common_upload(self._test_params.get("task_id"), source_value)
        assert response_upload.status_code == HTTPStatus.OK
        assert response_upload.json().get('success') == True
        time.sleep(10) # ждем скачивания документов, альтернатива таймеру - писать в тесте цикл while с запросом step

        step = self.waiting_page.step()
        self._test_params["current_view"] = step.json().get("contents", {}).get("view")
        assert self._test_params.get("current_view") == "FVNOPdfPreview"

        self.pdf_preview_page.get_files()
        self.pdf_preview_page.next(self._test_params.get("current_view"))
        step = self.document_primary_page.step()
        self._test_params["current_view"] = step.json().get("contents", {}).get("view")
        assert self._test_params.get("current_view") == "FVNOEmployeeConfirm"

        self.employee_confirm_page.get_client_document()
        self.employee_confirm_page.employee_confirm()
        self.employee_confirm_page.next(self._test_params.get("installer_code"), self._test_params.get("current_view"))
        step = self.employee_confirm_page.step()
        self._test_params["current_view"] = step.json().get("contents", {}).get("view")
        assert self._test_params.get("current_view") == "FVNOSignature"

        # TODO на Тесте нужно брать сгенерированный код смс подтверждения из БД
        self.client_signature_page.signature()
        self.client_signature_page.next(self._test_params.get("current_view"))
        step = self.client_signature_page.step()
        self._test_params["current_view"] = step.json().get("contents", {}).get("view")
        assert self._test_params.get("current_view") == "FVNOComplete"

        # UPLOAD
        response_upload = Upload.common_upload(self._test_params.get("task_id"), source_value)
        assert response_upload.status_code == HTTPStatus.OK
        assert response_upload.json().get('success') is True
        time.sleep(10) # ждем скачивания документов и завершения бизнес-процесса

        assert task_repository.get_task_status(self._test_params.get("task_id")) == 'COMPLETED'
        # TODO Вынести удаление задачи из БД в хуки
        task_repository.delete_task_by_task_id_from_all_tables(self._test_params.get("task_id"))

        # TODO проверка отсутствия ошибок в логе???
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
