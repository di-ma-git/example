import copy

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
    def modify_payload_body_for_client_validation(body, source_value, type_task, field, value):
        body_new = body.copy()
        body_new["data"]["key"] = str(random.randint(1000, 1000000))
        body_new["data"]["source"] = source_value
        body_new["data"]["type"] = type_task
        body_new["data"]["content"]["client"][field] = value

        return body_new


    @staticmethod
    def modify_payload_body_for_validation(body: dict, source_value: str, type_task: str, path_value: dict) -> dict:
        body_new = copy.deepcopy(body)
        body_new["data"]["key"] = str(random.randint(1000, 1000000))
        body_new["data"]["source"] = source_value
        body_new["data"]["type"] = type_task
        body_new["data"]["identificationValue"] = "9" + str(random.randint(100000000, 999999999))
        for field_path, value in path_value.items():
            keys = field_path.split(".")
            current = body_new["data"]

            for key in keys[1:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]

            if value == "отсутствует":
                if keys[-1] in current:
                    del current[keys[-1]]
            else:
                current[keys[-1]] = value

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










