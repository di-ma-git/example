import urls
from data import MultipartFormData
from data import Data
from data import Data_doc
import requests
import pytest
import helper
from api.create import Create


class TestCreateValidation:
    source_value = ['CRM_VOLGA_V3', 'CRM_SOUTH_V3', 'CRM_URAL_V3', 'CRM_NORTH_WEST_V3', 'CRM_FAR_EAST_V3',
                    'CRM_SIBERIA_V3']
    type_task = ['CONTRACT_EFD', 'CONVERGENT_SELF', 'CONTRACT_SIM_SELF', 'CONVERGENT_CRM']
    # type_doc = ['TEMPORARY_CERTIFICATE', 'OFFICER_CERTIFICATE', 'MILITARY_TICKET',
    #             'REFUGEE_CERTIFICATE', 'REFUGEE_IMMIGRANTS_CERTIFICATE', 'CERTIFICATE_OF_ASYLUM']

