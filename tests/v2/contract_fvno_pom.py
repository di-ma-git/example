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
import urls
import time
from requests import Session
from tests.v2.pom.base_api import BaseAPI
from tests.v2.pom.register_page import RegisterPage
from tests.v2.pom.login_page import LoginPage
from tests.v2.pom.offer_page import OfferPage
from tests.v2.pom.client_page import ClientPage
from tests.v2.pom.email_confirm_page import EmailConfirmPage



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
        self.offer_page.next(self._current_view) # падает тест, возможно надо добавить вейтинги или слипы, проверь работу ретраев
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
        task_repository.get_confirm_email_code_by_task_id(self._task_id)
        self.email_confirm_page.next(task_repository.get_confirm_email_code_by_task_id(self._task_id),
                                     self._current_view)
        step = self.email_confirm_page.step()
        self._current_view = step.json().get("contents", {}).get("view")
        assert self._current_view == "UniformDocumentPrimary"

        result_contract_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/contract?" +
            "fields%5B%5D=email",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_contract_get.status_code == HTTPStatus.OK
        assert result_contract_get.json().get("contents")
        time.sleep(1)

        result_email_confirm_post = requests.post(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/fvno/email-confirm",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_email_confirm_post.status_code == HTTPStatus.OK
        assert result_email_confirm_post.json().get("contents")
        time.sleep(1)

        # TODO взят из базы код для подтверждения email, записать в переменную
        self._confirm_email_code = task_repository.get_confirm_email_code_by_task_id(self._task_id)

        payload_email_confirm_next_post = {"data": {"code": f"{self._confirm_email_code}", "email": "maltsev.d@rt.ru"},
                                           "from": f"{self._view}"}

        result_email_confirm_next_post = requests.post(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/fvno/email-confirm/next",
            headers=self._headers_front_with_auth,
            json=payload_email_confirm_next_post,
            verify=False
        )
        assert result_email_confirm_next_post.status_code == HTTPStatus.OK
        assert result_email_confirm_next_post.json().get("status") == "success"
        time.sleep(1)

        result_step_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/step",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_step_get.status_code == HTTPStatus.OK
        assert result_step_get.json().get("contents", {}).get("view") == "UniformDocumentPrimary"
        self._view = result_step_get.json().get("contents", {}).get("view")
        time.sleep(1)

        result_nationality_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/contract?fields%5B%5D=nationality",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_nationality_get.status_code == HTTPStatus.OK
        assert result_nationality_get.json().get("contents", {}).get("nationality", {}).get(
            "value") == self._nationality
        time.sleep(1)

        result_document_primary_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/uniform/document-primary",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_document_primary_get.status_code == HTTPStatus.OK
        assert result_document_primary_get.json().get("contents", {}).get("document")
        time.sleep(1)

        payload_document_primary_next_get = {
            "data": {
                "document": {
                    "type": "PASSPORT_RU",
                    "affiliation": "CLIENT",
                    "fullName": None,
                    "series": "1814",
                    "number": "979498",
                    "departmentCode": "760-014",
                    "placeOfIssue": "УМВД",
                    "dateOfIssue": "06.04.2015",
                    "expirationDate": None,
                    "dateOfBirth": "03.12.1991",
                    "placeOfBirth": "Нижний Новгород",
                    "readOnly": [
                        "series",
                        "number"
                    ]
                }
            },
            "from": "UniformDocumentPrimary"
        }
        result_document_primary_next_get = requests.post(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/uniform/document-primary/next",
            headers=self._headers_front_with_auth,
            json=payload_document_primary_next_get,
            verify=False
        )
        assert result_document_primary_next_get.status_code == HTTPStatus.OK
        assert result_email_confirm_next_post.json().get("status") == "success"
        time.sleep(1)

        result_step_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/step",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_step_get.status_code == HTTPStatus.OK
        assert result_step_get.json().get("contents", {}).get("view") == "FVNOAddress"
        self._view = result_step_get.json().get("contents", {}).get("view")
        time.sleep(1)

        result_contract_addresses_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/contract?" +
            "fields%5B%5D=installationAddressFlat&" +
            "fields%5B%5D=installationAddressGlobalId&" +
            "fields%5B%5D=installationAddressHouse&" +
            "fields%5B%5D=installationAddressManual&" +
            "fields%5B%5D=installationAddressRegion&" +
            "fields%5B%5D=installationAddressStreet&" +
            "fields%5B%5D=installationAddressSuggestions&" +
            "fields%5B%5D=installationAddressTown&" +
            "fields%5B%5D=installationAddressZipCode&" +
            "fields%5B%5D=nationality&" +
            "fields%5B%5D=registrationAddressFlat&" +
            "fields%5B%5D=registrationAddressGlobalId&" +
            "fields%5B%5D=registrationAddressHouse&" +
            "fields%5B%5D=registrationAddressManual&" +
            "fields%5B%5D=registrationAddressRegion&" +
            "fields%5B%5D=registrationAddressStreet&" +
            "fields%5B%5D=registrationAddressSuggestions&" +
            "fields%5B%5D=registrationAddressTown&" +
            "fields%5B%5D=registrationAddressZipCode",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_contract_addresses_get.status_code == HTTPStatus.OK
        assert result_contract_addresses_get.json().get("contents")
        time.sleep(1)

        payload_next_post = {
            "data": {
                "registrationAddressFlat": f"{result_contract_addresses_get.json().get("contents", {}).get("registrationAddressFlat", {}).get("value")}",
                "registrationAddressGlobalId": f"{result_contract_addresses_get.json().get("contents", {}).get("registrationAddressGlobalId", {}).get("value")}",
                "registrationAddressHouse": f"{result_contract_addresses_get.json().get("contents", {}).get("registrationAddressHouse", {}).get("value")}",
                "registrationAddressManual": f"{result_contract_addresses_get.json().get("contents", {}).get("registrationAddressManual", {}).get("value")}",
                "registrationAddressRegion": f"{result_contract_addresses_get.json().get("contents", {}).get("registrationAddressRegion", {}).get("value")}",
                "registrationAddressStreet": f"{result_contract_addresses_get.json().get("contents", {}).get("registrationAddressStreet", {}).get("value")}",
                "registrationAddressSuggestions": f"{result_contract_addresses_get.json().get("contents", {}).get("registrationAddressSuggestions", {}).get("value")}",
                "registrationAddressTown": f"{result_contract_addresses_get.json().get("contents", {}).get("registrationAddressTown", {}).get("value")}",
                "registrationAddressZipCode": f"{result_contract_addresses_get.json().get("contents", {}).get("registrationAddressZipCode", {}).get("value")}"
            },
            "from": f"{self._view}"
        }
        result_next_post = requests.post(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/fvno/offer/next",
            headers=self._headers_front_with_auth,
            json=payload_next_post,
            verify=False
        )
        assert result_next_post.status_code == HTTPStatus.OK
        assert result_next_post.json().get("status") == "success"
        time.sleep(1)

        result_step_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/step",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_step_get.status_code == HTTPStatus.OK
        assert result_step_get.json().get("contents", {}).get("view") == "FVNOEquipment"
        self._view = result_step_get.json().get("contents", {}).get("view")
        time.sleep(1)

        result_equipment_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/fvno/equipment",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_equipment_get.status_code == HTTPStatus.OK
        assert result_equipment_get.json().get("contents")
        time.sleep(1)

        payload_alternative_post = {"from": f"{self._view}"}
        result_alternative_post = requests.post(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/fvno/equipment/alternative",
            headers=self._headers_front_with_auth,
            json=payload_alternative_post,
            verify=False
        )
        assert result_alternative_post.status_code == HTTPStatus.OK
        assert result_alternative_post.json().get("status") == "success"
        time.sleep(1)

        result_step_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/step",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_step_get.status_code == HTTPStatus.OK
        assert result_step_get.json().get("contents", {}).get("view") == "FVNOWaiting"
        self._view = result_step_get.json().get("contents", {}).get("view")
        time.sleep(3)

        # UPLOAD
        result_upload_post = requests.post(
            f"{urls.BASE_URL_DEV}{urls.CREATE_TASK}{self._task_id}{urls.UPLOAD}",
            headers=Data.headers2,
            json=Data.data_upload_file_links_ural,
            verify=False
        )
        assert result_upload_post.status_code == HTTPStatus.OK
        assert result_upload_post.json().get('success') == True

        # TODO возможно тут нужен waiting
        time.sleep(10)

        result_step_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/step",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_step_get.status_code == HTTPStatus.OK
        assert result_step_get.json().get("contents", {}).get("view") == "FVNOPdfPreview"
        self._view = result_step_get.json().get("contents", {}).get("view")
        time.sleep(1)

        result_contract_files_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/contract?fields%5B%5D=files",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_contract_files_get.status_code == HTTPStatus.OK
        assert result_contract_files_get.json().get("contents")
        time.sleep(1)

        payload_pdf_preview_next_post = {"from": f"{self._view}"}
        result_pdf_preview_next_post = requests.post(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/fvno/pdf-preview/next",
            headers=self._headers_front_with_auth,
            json=payload_pdf_preview_next_post,
            verify=False
        )
        assert result_pdf_preview_next_post.status_code == HTTPStatus.OK
        assert result_pdf_preview_next_post.json().get("status") == "success"
        time.sleep(1)

        result_step_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/step",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_step_get.status_code == HTTPStatus.OK
        assert result_step_get.json().get("contents", {}).get("view") == "FVNOEmployeeConfirm"
        self._view = result_step_get.json().get("contents", {}).get("view")
        time.sleep(1)

        result_contract_installer_confirm_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/contract?" +
            "fields%5B%5D=attorney&" +
            "fields%5B%5D=attorneyDocument&" +
            "fields%5B%5D=documentPrimary&" +
            "fields%5B%5D=documentSecondary&" +
            "fields%5B%5D=middleName&" +
            "fields%5B%5D=name&" +
            "fields%5B%5D=surname",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_contract_installer_confirm_get.status_code == HTTPStatus.OK
        assert result_contract_installer_confirm_get.json().get("contents")
        time.sleep(1)

        result_contract_employee_confirm_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/fvno/employee-confirm",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_contract_employee_confirm_get.status_code == HTTPStatus.OK
        assert result_contract_employee_confirm_get.json().get("contents")
        time.sleep(1)

        payload_employee_confirm_next_post = {"data": {"code": f"{self._installer_code}"}, "from": f"{self._view}"}
        result_employee_confirm_next_post = requests.post(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/fvno/employee-confirm/next",
            headers=self._headers_front_with_auth,
            json=payload_employee_confirm_next_post,
            verify=False
        )
        assert result_employee_confirm_next_post.status_code == HTTPStatus.OK
        assert result_employee_confirm_next_post.json().get("status") == "success"
        time.sleep(1)

        result_step_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/step",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_step_get.status_code == HTTPStatus.OK
        assert result_step_get.json().get("contents", {}).get("view") == "FVNOSignature"
        self._view = result_step_get.json().get("contents", {}).get("view")
        time.sleep(1)

        result_signature_post = requests.post(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/fvno/signature",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_signature_post.status_code == HTTPStatus.OK
        assert result_signature_post.json().get("contents")
        time.sleep(1)
        # TODO возможно нужно взять код смс подтверждения из базы

        payload_signature_next_post = {"data": {"code": "333333"}, "from": f"{self._view}", "source": "web"}
        result_signature_next_post = requests.post(
            "http://devapp.homeinternet.rt.ru/api/v1/contract/fvno/signature/next",
            headers=self._headers_front_with_auth,
            json=payload_signature_next_post,
            verify=False
        )
        assert result_signature_next_post.status_code == HTTPStatus.OK
        assert result_signature_next_post.json().get("status") == "success"
        time.sleep(1)

        result_step_get = requests.get(
            "http://devapp.homeinternet.rt.ru/api/v1/step",
            headers=self._headers_front_with_auth,
            verify=False
        )
        assert result_step_get.status_code == HTTPStatus.OK
        assert result_step_get.json().get("contents", {}).get("view") == "FVNOComplete"
        self._view = result_step_get.json().get("contents", {}).get("view")
        time.sleep(3)

        # UPLOAD
        result_upload_post = requests.post(
            f"{urls.BASE_URL_DEV}{urls.CREATE_TASK}{self._task_id}{urls.UPLOAD}",
            headers=Data.headers2,
            json=Data.data_upload_file_links_ural,
            verify=False
        )
        assert result_upload_post.status_code == HTTPStatus.OK
        assert result_upload_post.json().get('success') == True
        time.sleep(10)

        assert task_repository.get_task_status(self._task_id) == 'COMPLETED'
        task_repository.delete_task_by_task_id_from_all_tables(self._task_id)

        # TODO проверить статус задачи COMPLETED  базе
        # TODO отсутствие ошибок в логе
        # TODO проверить логи выборочно???
        # TODO проверить токен в камунде??? через базу или через api???

    source_value = ['CRM_SIBERIA_V2']
    type_task = ['CONTRACT_FVNO']
    provider_value = ['TINKOFF']

    @pytest.mark.parametrize('source_value', source_value)
    @pytest.mark.parametrize('type_task', type_task)
    @pytest.mark.parametrize('provider_value', provider_value)
    def test_e2e_contract_fvno_siberia(self, source_value, type_task, provider_value):
        pass
