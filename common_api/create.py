import urls
from data import MultipartFormData
from data import Data
import requests
import pytest
import helper


class Create:

    @staticmethod
    def create_and_cancel(data):
        mh = MultipartFormData.format(data=data, headers=Data.headers)
        url = urls.BASE_URL_DEV + urls.CREATE_TASK
        response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
        print(response.text)
        if not response.json()["success"]:
            temp = response.json()["error"]
            url1 = url + temp['taskId'] + "/cancel?reason=OK"
            print(url1)
            requests.request("POST", url1, headers=Data.headers1, verify=False)
            mh = MultipartFormData.format(data=data, headers=Data.headers)
            url = urls.BASE_URL_DEV + urls.CREATE_TASK
            response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
            print(response.text)
        url1 = url + response.json()["taskId"] + "/cancel?reason=OK"
        print(url1)
        requests.request("POST", url1, headers=Data.headers1, verify=False)
        return response

    @staticmethod
    def create_and_cancel_v3(data):
        mh = MultipartFormData.format(data=data, headers=Data.headers)
        url = urls.BASE_URL_DEV + urls.CREATE_TASK_V3
        response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
        print(response.text)
        if not response.json()["success"]:
            temp = response.json()["error"]
            url1 = url + temp['taskId'] + "/cancel?reason=OK"
            print(url1)
            requests.request("POST", url1, headers=Data.headers1, verify=False)
            mh = MultipartFormData.format(data=data, headers=Data.headers)
            url = urls.BASE_URL_DEV + urls.CREATE_TASK_V3
            response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
            print(response.text)
        url1 = url + response.json()["taskId"] + "/cancel?reason=OK"
        print(url1)
        requests.request("POST", url1, headers=Data.headers1, verify=False)
        return response

    @staticmethod
    def create_for_e2e_v2(data):
        mh = MultipartFormData.format(data=data, headers=Data.headers)
        url = urls.BASE_URL_DEV + urls.CREATE_TASK
        response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
        print(response.text)
        if not response.json()["success"]:
            temp = response.json()["error"]
            url1 = url + temp['taskId'] + "/cancel?reason=OK"
            print(url1)
            requests.request("POST", url1, headers=Data.headers1, verify=False)
            mh = MultipartFormData.format(data=data, headers=Data.headers)
            url = urls.BASE_URL_DEV + urls.CREATE_TASK
            response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
            print(response.text)
        return response
    @staticmethod
    def create_for_e2e_v3(data):
        mh = MultipartFormData.format(data=data, headers=Data.headers)
        url = urls.BASE_URL_DEV + urls.CREATE_TASK_V3
        response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
        print(response.text)
        if not response.json()["success"]:
            temp = response.json()["error"]
            url1 = url + temp['taskId'] + "/cancel?reason=OK"
            print(url1)
            requests.request("POST", url1, headers=Data.headers1, verify=False)
            mh = MultipartFormData.format(data=data, headers=Data.headers)
            url = urls.BASE_URL_DEV + urls.CREATE_TASK_V3
            response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
            print(response.text)
        return response

    @staticmethod
    def create_and_cancel_for_wrapper_v2(data, file_info):
        combined_data = {'data': data['data'], 'fileInfo': file_info['fileInfo']}
        mh = MultipartFormData.format(data=combined_data, headers=Data.headers)

        url = urls.BASE_URL_DEV + urls.CREATE_TASK_V2
        response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
        print(response.text)
        if not response.json()["success"]:
            temp = response.json()["error"]
            url1 = url + temp['taskId'] + "/cancel?reason=OK"
            print(url1)
            requests.request("POST", url1, headers=Data.headers1, verify=False)
            mh = MultipartFormData.format(data=combined_data, headers=Data.headers)
            url = urls.BASE_URL_DEV + urls.CREATE_TASK_V2
            response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
            print(response.text)
        url1 = url + response.json()["taskId"] + "/cancel?reason=OK"
        print(url1)
        requests.request("POST", url1, headers=Data.headers1, verify=False)
        return response

    @staticmethod
    def create_for_search(data):
        mh = MultipartFormData.format(data=data, headers=Data.headers)
        url = urls.BASE_URL_DEV + urls.CREATE_TASK
        response = requests.request("POST", url, headers=Data.headers, data=mh, verify=False)
        print(response.text)
        return response
