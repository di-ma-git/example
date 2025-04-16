import json

branch = "80"
account = "300300400500"
nationality = "RUS"
phone = "9333333331"


class Data_doc:
    DATA_ATTORNEY = [['CONTRACT', 'CRM_VOLGA_V2'], ['PAID_WORK_ACT', 'CRM_VOLGA_V2'], ['CONTRACT', 'CRM_SOUTH_V2'],
                     ['PAID_WORK_ACT', 'CRM_SOUTH_V2'], ['PAID_WORK_ACT', 'CRM_URAL_V2'],
                     ['CONTRACT', 'CRM_NORTH_WEST_V2'], ['CONVERGENT', 'CRM_NORTH_WEST_V2'],
                     ['CONTRACT_DZO', 'CRM_NORTH_WEST_V2'], ['PAID_WORK_ACT', 'CRM_NORTH_WEST_V2'],
                     ['PAID_WORK_ACT', 'CRM_FAR_EAST_V2'], ['PAID_WORK_ACT', 'CRM_SIBERIA_V2']]

    DATA_TEMPORARY_CERTIFICATE_AND_CO = [['PAID_WORK_ACT', 'CRM_VOLGA_V2'], ['CONTRACT', 'CRM_SOUTH_V2'],
                                         ['PAID_WORK_ACT', 'CRM_SOUTH_V2'],
                                         ['PAID_WORK_ACT', 'CRM_URAL_V2'], ['CONTRACT', 'CRM_NORTH_WEST_V2'],
                                         ['CONVERGENT', 'CRM_NORTH_WEST_V2'], ['CONTRACT_DZO', 'CRM_NORTH_WEST_V2'],
                                         ['PAID_WORK_ACT', 'CRM_NORTH_WEST_V2'], ['CONTRACT', 'CRM_FAR_EAST_V2'],
                                         ['PAID_WORK_ACT', 'CRM_FAR_EAST_V2'], ['PAID_WORK_ACT', 'CRM_SIBERIA_V2']]

    DATA_TEMPMILITARYID = [['PAID_WORK_ACT', 'CRM_VOLGA_V2'], ['CONTRACT', 'CRM_SOUTH_V2'],
                           ['PAID_WORK_ACT', 'CRM_SOUTH_V2'],
                           ['PAID_WORK_ACT', 'CRM_URAL_V2'],
                           ['PAID_WORK_ACT', 'CRM_NORTH_WEST_V2'], ['CONTRACT', 'CRM_FAR_EAST_V2'],
                           ['PAID_WORK_ACT', 'CRM_FAR_EAST_V2'], ['PAID_WORK_ACT', 'CRM_SIBERIA_V2']]

    DATA_PASSPORT_FOREIGNER = [['PAID_WORK_ACT', 'CRM_VOLGA_V2'], ['CONTRACT', 'CRM_SOUTH_V2'],
                               ['PAID_WORK_ACT', 'CRM_SOUTH_V2'],
                               ['PAID_WORK_ACT', 'CRM_URAL_V2'],
                               ['PAID_WORK_ACT', 'CRM_NORTH_WEST_V2'],
                               ['PAID_WORK_ACT', 'CRM_FAR_EAST_V2'], ['PAID_WORK_ACT', 'CRM_SIBERIA_V2']]


class MultipartFormData(object):
    "" "преобразование формата multipart / form-data" ""

    @staticmethod
    def format(data: dict, boundary: str = "----WebKitFormBoundary7MA4YWxkTrZu0gW", headers=None) -> str:
        if headers is None:
            headers = {}
        if "content-type" in headers:
            fd_val = str(headers.get("content-type", ""))
            if "boundary" in fd_val:
                boundary = fd_val.split(";")[1].strip().split("=")[1].strip()
            else:
                raise ValueError(
                    "Информация заголовка multipart/form-data неверна, проверьте, содержит ли ключ типа содержимого границу")

        if not isinstance(data, dict):
            raise TypeError("Ошибка параметра multipart/form-data, параметр данных должен иметь тип dict")

        json_str_template = '--{}\r\nContent-Disposition: form-data; name="{}"\r\nContent-Type: application/json\r\n\r\n{}\r\n'
        end_str = "--{}--".format(boundary)
        args_str = ""

        for key, value in data.items():
            json_value = json.dumps(value, ensure_ascii=False)
            args_str += json_str_template.format(boundary, key, json_value)

        args_str += end_str.format(boundary)
        return args_str.replace("\'", "\"")


class Data:
    data_wrapper = {
        "data": {
            "type": "SIGNING_DOCUMENTS_WRAPPER",
            "branch": "82",
            "source": "CRM_MOSCOW_V3",
            "key": "474",
            "identificationParameter": "PHONE",
            "identificationValue": "9013117197",
            "content": {
                "contract": {
                    "account": "452020383987"
                },
                "client": {
                    "name": "Дмитрий",
                    "middleName": "Сергеевич",
                    "surname": "Мальцев",
                    "nationality": "RUS",
                    "snils": "",
                    "inn": "",
                    "phone": "9229612909",
                    "email": "maltsev.d@rt.ru"
                },
                "documents": [
                    {
                        "type": "PASSPORT_RU",
                        "series": "1814",
                        "number": "979498",
                        "placeOfIssue": "УМВД",
                        "dateOfIssue": "06.04.2015"
                    }
                ]
            }
        }
    }

    file_info_wrapper = {
        "fileInfo": {
            "info": [
                {
                    "fileType": "remotesite",
                    "idMrf": "2030260c-82a2-42e6-a394-9e50fcc17c31",
                    "path": "http://10.42.110.215:8759/ed-plugs/file&if=maincontract.pdf"
                },
                {
                    "fileType": "remoteSiteAct",
                    "idMrf": "2030260c-82a2-42e6-a394-9e50fcc17c31",
                    "path": "http://10.42.110.215:8759/ed-plugs/file&if=maincontract.pdf"
                }
            ]
        }
    }

    data_contract_efd_v3 = {
        "data": {
            "type": "",
            "source": "",
            "branch": branch,
            "key": "",
            "identificationParameter": "PHONE",
            "identificationValue": phone,
            "content": {
                "contract": {
                    "paymentMethod": "CREDIT",
                    "deliveryMethod": "EMAIL",
                    "consentToReceiveAdvertising": "true",
                    "consentToSmsInform": "true",
                    "consentToUseSubscriberData": "true",
                    "account": account,
                    "installerCode": "1234"
                },
                "client": {
                    "phone": "9993000299",
                    "sex": "FEMALE",
                    "email": "olga.y.belova@volga.rt.ru",
                    "nationality": nationality
                },
                "documents": [
                    {
                        "type": "PASSPORT_RU",
                        "affiliation": "CLIENT"
                    }],
                "registrationAddress": {
                    "globalId": 4046576
                },
                "installationAddress": {
                    "globalId": 4046576
                },
                "wfm": {
                    "order": "2148312248"
                },
                "payment": {
                    "startPayment": 699.0,
                    "link": "https://lk.rt.ru/new/#payment",
                    "firstPaymentDays": 5
                },
                "equipment": {
                    "installmentTotalCost": 5,
                    "rentGuaranteePlus": True,
                    "ownedGuaranteePlus": True,
                    "devices": [
                        {
                            "categoryName": "Умные устройства",
                            "transferTermName": "Продажа",
                            "deviceName": "Умная колонка",
                            "deviceSerialNumber": "564-as-963",
                            "deviceCondition": "новое",
                            "cost": 6000.0,
                            "promotionCost": 5000.0,
                            "promotionName": "Сдай старую колонку и получи скидку 1000р на покупку новой",
                            "regularPayment": 400,
                            "installmentPeriod": 12,
                            "paymentTerms": "в рассрочку",
                            "firstPayment": 600,
                            "guaranteePlusOneTimeCost": 1000.0,
                            "guaranteePlusTemporary": False,
                            "guaranteePlusIndefinitely": 555
                        }
                    ]
                },
                "contractDocuments": [
                    {
                        "blanks": [
                            "CONTRACT",
                            "ANNEXSERVICE",
                            "ANNEXEQUIPMENTOWNED",
                            "ANNEXEQUIPMENTRENT",
                            "MNPREQUEST"
                        ],
                        "archiveParameters": {
                            "docType": "EDOCONTRACT",
                            "parameters": {
                                "clientName": "Алексеев Дмитрий Сергеевич",
                                "serviceId": [
                                    {
                                        "name": "ШПД",
                                        "value": "3"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "blanks": [
                            "ANNEXWORK"
                        ],
                        "archiveParameters": {
                            "docType": "ACTOTHER",
                            "parameters": {
                                "clientName": "Алексеев Дмитрий Сергеевич",
                                "serviceId": [
                                    {
                                        "name": "Прочее",
                                        "value": "15"
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
        }
    }

    data_convergent_self_v3 = {
        "data": {
            "type": "",
            "source": "",
            "provider": "",
            "product": "",
            "branch": branch,
            "key": "",
            "identificationParameter": "PHONE",
            "identificationValue": phone,
            "content": {
                "contract": {
                    "paymentMethod": "CREDIT",
                    "deliveryMethod": "EMAIL",
                    "consentToReceiveAdvertising": "true",
                    "consentToSmsInform": "true",
                    "consentToUseSubscriberData": "true",
                    "account": account
                },
                "client": {
                    "name": "Дмитрий",
                    "surname": "Мальцев",
                    "middleName": "Сергеевич",
                    "phone": "9993000299",
                    "sex": "MALE",
                    "email": "maltsev.d@rt.ru",
                    "nationality": nationality
                },
                "documents": [
                    {
                        "type": "PASSPORT_RU",
                        "affiliation": "CLIENT",
                        "series": "3304",
                        "number": "499688"
                    }],
                "registrationAddress": {
                    "globalId": 4046576
                },
                "installationAddress": {
                    "globalId": 4046576
                },
                "wfm": {
                    "order": "2148312248"
                }

            }
        }
    }

    data_convergent_crm_v3 = {
        "data": {
            "type": "",
            "source": "",
            "branch": branch,
            "key": "",
            "identificationParameter": "PHONE",
            "identificationValue": phone,
            "content": {
                "contract": {
                    "paymentMethod": "CREDIT",
                    "deliveryMethod": "EMAIL",
                    "consentToReceiveAdvertising": "true",
                    "consentToSmsInform": "true",
                    "consentToUseSubscriberData": "true",
                    "account": account,
                    "installerCode": "123456",
                    "contractDate": "12.07.2024",
                    "contractNumber": "123412"

                },
                "client": {
                    "phone": "9993000299",
                    "sex": "FEMALE",
                    "email": "olga.y.belova@volga.rt.ru",
                    "nationality": ""
                },
                "registrationAddress": {
                    "globalId": 4046576
                },
                "installationAddress": {
                    "globalId": 4046576
                },
                "transfer": {
                    "totalCost": "",
                    "transferredEquipments": [
                        {
                            "equipmentName": "AQ",
                            "equipmentSerialNumber": "564",
                            "equipmentMacAddress": "f5.454.323.456.35",
                            "equipmentCondition": "new",
                            "equipmentPrice": "0",
                            "installment": {
                                "firstPayment": "0",
                                "installmentTerm": "3",
                                "installmentPlan": "new plan",
                                "regularPayment": "555.99",
                                "firstPaymentDate": "25.07.2024",
                                "lastPaymentDate": "28.07.2024"
                            }
                        }
                    ]
                }
            }
        }
    }

    data_contract_sim_self_v3 = {
        "data": {
            "type": "",
            "source": "",
            "branch": branch,
            "key": "",
            "identificationParameter": "PHONE",
            "identificationValue": phone,
            "content": {
                "contract": {
                    "paymentMethod": "CREDIT",
                    "deliveryMethod": "EMAIL",
                    "consentToReceiveAdvertising": "true",
                    "consentToSmsInform": "true",
                    "consentToUseSubscriberData": "true",
                    "installerCode": "123456"
                },
                "client": {
                    "phone": "9993000299",
                    "sex": "FEMALE",
                    "email": "olga.y.belova@volga.rt.ru",
                    "nationality": nationality
                },
                "documents": [
                    {
                        "type": "PASSPORT_RU",
                        "affiliation": "CLIENT"
                    }],
                "registrationAddress": {
                    "globalId": 4046576
                },
                "installationAddress": {
                    "globalId": 4046576
                },
                "wfm": {
                    "order": 2148312248
                }

            }
        }
    }

    data_contract_fvno = {
        "data": {
            "type": "CONTRACT_FVNO",
            "branch": "36",
            "source": "CRM_URAL_V2",
            "key": "441",
            "provider": "TINKOFF",
            "product": "ANY_PRODUCT",
            "identificationParameter": "PHONE",
            "identificationValue": "9023111180",
            "content": {
                "signature": {
                    "oid": "565651032465233533"
                },
                "meta": [
                    {
                        "fields": [
                            "client.sex"
                        ],
                        "modifiers": [
                            "READ_ONLY"
                        ]
                    }
                ],
                "contract": {
                    "account": "452020383464",
                    "paymentMethod": "CREDIT",
                    "deliveryMethodElk": True,
                    "deliveryMethodEmail": False,
                    "deliveryMethodPost": False,
                    "consentToReceiveAdvertising": True,
                    "consentToSmsInform": False,
                    "consentToUseSubscriberData": True,
                    "consentToDigitalContract": False,
                    "consentToThirdParty": False,
                    "consentToUseConfidantData": False,
                    "installerCode": "1234",
                    "contractNumber": "",
                    "contractDate": None
                },
                "client": {
                    "name": "Дмитрий",
                    "middleName": "Сергеевич",
                    "surname": "Мальцев",
                    "sex": "MALE",
                    "nationality": "RUS",
                    "inn": "",
                    "codeWord": "ПОКА",
                    "phone": "9229612909",
                    "email": "maltsev.d@rt.ru",
                    "beneficiary": False,
                    "publicOfficial": False
                },
                "documents": [
                    {
                        "type": "PASSPORT_RU",
                        "affiliation": "CLIENT",
                        "series": "1814",
                        "number": "979498",
                        "departmentCode": "760-014",
                        "placeOfIssue": "УМВД",
                        "placeOfBirth": "г. Нижний Новгород",
                        "fullName": None,
                        "dateOfIssue": "06.04.2015",
                        "expirationDate": None,
                        "dateOfBirth": "03.12.1991",
                        "readOnly": [
                            "series",
                            "number"
                        ]
                    }
                ],
                "registrationAddress": {
                    "globalId": "1234567",
                    "zipCode": "363750",
                    "region": "Респ Северная Осетия - Алания, Моздокский р-н",
                    "town": "г Моздок",
                    "street": "ул Ленина",
                    "house": "д 18",
                    "corpus": "",
                    "building": "",
                    "flat": "31",
                    "suggestions": None,
                    "manual": False
                },
                "installationAddress": {
                    "globalId": "18302401",
                    "zipCode": "363750",
                    "region": "Респ Северная Осетия - Алания, Моздокский р-н ЮГ В3",
                    "town": "г Моздок",
                    "street": "ул Ленина",
                    "house": "д 18",
                    "corpus": "",
                    "building": "",
                    "flat": "23",
                    "suggestions": None,
                    "manual": False
                },
                "invoiceAddress": None,
                "wfm": {
                    "order": "7018863326",
                    "equipments": [
                        {
                            "requirementId": "oss#477775857wfm",
                            "cpeOrderId": None,
                            "equipmentName": "Терминал оптический линейный TS-1001GF RJ45wfmm",
                            "modelName": "Терминал оптический линейный TS-1001GF RJ45wfmmm",
                            "nomenclatureCode": "066.5600.Q416",
                            "categoryName": "ONT",
                            "serialNumber": "545253522448283B",
                            "usedOption": "новое",
                            "transferTermName": "",
                            "usedState": "Новое",
                            "price": None,
                            "warrantyEndDate": None,
                            "promotionCost": None,
                            "promotionName": None,
                            "regularPayment": None,
                            "rentPeriod": None,
                            "promotionRegularPayment": None,
                            "promotionPeriod": None,
                            "installmentPeriod": None,
                            "paymentTerms": None,
                            "firstPayment": None,
                            "installmentPlan": None,
                            "firstPaymentDate": None,
                            "lastPaymentDate": None,
                            "guaranteePlusOneTimeCost": None,
                            "guaranteePlusMonthlyCost": None,
                            "guaranteePlusIndefinitely": False,
                            "guaranteePlusTemporary": False
                        }
                    ]
                },
                "payment": {
                    "startPayment": 699.0,
                    "link": "https://lk.rt.ru/new/#payment",
                    "dateOfExpire": None,
                    "account": "268945623493"
                }
            }
        }
    }

    headers_multipart_form_data = {
        'Authorization': 'Basic ZWRfcWFfdGVzdDpDZTFCJFRNc1ZFaU0=',
        'User-Agent': 'PostmanRuntime/7.23.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Postman-Token': 'f6b7900a-c687-405d-a3f6-5467018c736b',
        'Host': 'devapi.ed.rt.ru',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'JSESSIONID=4476582DF6A963142434BCDCF3AACCE1',
        'Content-Length': '470',
        'Connection': 'keep-alive'
    }

    headers_application_json = {
        'Authorization': 'Basic ZWRfcWFfdGVzdDpDZTFCJFRNc1ZFaU0=',
        'User-Agent': 'PostmanRuntime/7.23.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Postman-Token': 'f6b7900a-c687-405d-a3f6-5467018c736b',
        'Host': 'devapi.ed.rt.ru',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'JSESSIONID=4476582DF6A963142434BCDCF3AACCE1',
        'Content-Length': '470',
        'Connection': 'keep-alive'
    }

    headers_authorization_only = {
        'Authorization': 'Basic ZWRfdXJhbF90ZXN0OmJ+VHkzYXRub2d7V3hEayM='
    }

    headers = {
        'Authorization': 'Basic ZWRfcWFfdGVzdDpDZTFCJFRNc1ZFaU0=',
        'User-Agent': 'PostmanRuntime/7.23.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Postman-Token': 'f6b7900a-c687-405d-a3f6-5467018c736b',
        'Host': 'devapi.ed.rt.ru',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'JSESSIONID=4476582DF6A963142434BCDCF3AACCE1',
        'Content-Length': '470',
        'Connection': 'keep-alive'
    }

    headers2 = {
        'Authorization': 'Basic ZWRfcWFfdGVzdDpDZTFCJFRNc1ZFaU0=',
        'User-Agent': 'PostmanRuntime/7.23.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Postman-Token': 'f6b7900a-c687-405d-a3f6-5467018c736b',
        'Host': 'devapi.ed.rt.ru',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'JSESSIONID=4476582DF6A963142434BCDCF3AACCE1',
        'Content-Length': '470',
        'Connection': 'keep-alive'
    }

    headers1 = {
        'Authorization': 'Basic ZWRfdXJhbF90ZXN0OmJ+VHkzYXRub2d7V3hEayM='
    }

    headers_front = {
        "Accept-Charset": "utf-8",
        'Accept': 'application/json; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json'
    }

    data_upload_file_links_ural = \
        [
            {
                "type": "MAINCONTRACT",
                "link": "http://10.42.110.215:8759/ed-plug/file?id=dogovorTinkoff.pdf",
                "displayName": "Договор",
                "parameters": {
                    "serviceId": [
                        {
                            "value": "3",
                            "name": "шпд"
                        }
                    ],
                    "clientName": "БУКИНА ЛЮБОВЬ АЛЕКСАНДРОВНА",
                    "contractNumber": "13535425"
                }
            }
        ]

    data_upload_file_links = \
        [
            {
                "type": "MAINCONTRACT",
                "link": "http://10.42.110.215:8759/ed-plug/file?id=dogovorTinkoff.pdf",
                "displayName": "Договор"
            }
        ]
