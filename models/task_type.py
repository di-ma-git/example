from enum import Enum
from typing import Type, ClassVar


class TaskType(Enum):
    CONTRACT = ("CONTRACT", True)
    CONTRACT_ALADDIN = ("CONTRACT_ALADDIN", False)
    CONTRACT_MEGAFON = ("CONTRACT_MEGAFON", False)
    CONTRACT_DZO = ("CONTRACT_DZO", False)
    CONVERGENT = ("CONVERGENT", True)
    TERMINATION = ("TERMINATION", True)
    RENEWAL = ("RENEWAL", True)
    CONTRACT_SIM_V2 = ("CONTRACT_SIM_V2", False)
    PAID_WORK_ACT = ("PAID_WORK_ACT", False)
    MNP = ("MNP", True)
    MNP_CRM = ("MNP_CRM", False)
    TRANSFER_ACT = ("TRANSFER_ACT", False)
    CONTRACT_SIM_SELF = ("CONTRACT_SIM_SELF", False)
    CONVERGENT_SELF = ("CONVERGENT_SELF", False)
    CONVERGENT_CRM = ("CONVERGENT_CRM", False)
    CONTRACT_EFD = ("CONTRACT_EFD", False)
    CONTRACT_FVNO = ("CONTRACT_FVNO", False)
    SIGNING_DOCUMENT_WRAPPER = ("SIGNING_DOCUMENT_WRAPPER", False)
    NONE = ("NONE", False)

    def __init__(self, type_name: str, has_source: bool):
        self._type_name = type_name
        self._has_source = has_source

    @property
    def name(self) -> str:
        return self._type_name

    @property
    def has_source(self) -> bool:
        return self._has_source

    @classmethod
    def find_task_type_by_name(cls: Type['TaskType'], name: str) -> 'TaskType':

        for task_type in cls:
            if name == task_type.name:
                return task_type
        return cls.NONE

    def __str__(self) -> str:
        return self.name
