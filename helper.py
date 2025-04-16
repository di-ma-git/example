import requests
from data import MultipartFormData
from data import Data
import random
import urls
import uuid

class Metods:
    @staticmethod
    def download(taskId):
        mh = MultipartFormData.format(data=Data.data_download, headers=Data.headers1)
        url = urls.BASE_URL_DEV + urls.CREATE_TASK + taskId + urls.UPLOAD
        print(url)
        response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
        print(response.text)


class ChangeTestDataHelper:
    @staticmethod
    def modify_payload_body(body, source_value, type_task):
        body_new = body.copy()
        body_new["data"]["key"] = str(random.randint(1000, 1000000))
        body_new["data"]["identificationValue"] = "9" + str(random.randint(100000000, 999999999))
        body_new["data"]["source"] = source_value
        body_new["data"]["type"] = type_task

        return body_new

    @staticmethod
    def modify_payload_body_file_info(file_info, file_type):
        file_info_new = file_info.copy()
        for item in file_info_new["fileInfo"]["info"]:
            item["fileType"] = file_type
        for item in file_info_new["fileInfo"]["info"]:
            item["idMrf"] = str(uuid.uuid4())

        return file_info_new
    @staticmethod
    def modify_payload_body_for_validation(body, source_value, type_task, email):
        body_new = body.copy()
        body_new["data"]["key"] = str(random.randint(1000, 1000000))
        body_new["data"]["source"] = source_value
        body_new["data"]["type"] = type_task
        body_new["data"]["content"]["client"]["email"] = email

        return body_new

    @staticmethod
    def modify_payload_fvno(body, source_value, type_task, provider_value):
        body_new = body.copy()
        body_new["data"]["key"] = str(random.randint(1000, 1000000))
        body_new["data"]["identificationValue"] = "9" + str(random.randint(100000000, 999999999))
        body_new["data"]["source"] = source_value
        body_new["data"]["type"] = type_task
        body_new["data"]["provider"] = provider_value

        return body_new










