import uuid
from task_type import TaskType


class Data:
    branch: str
    type: TaskType
    source: Source
    provider: str
    product: str
    key: str
    mainTaskId: uuid
    identificationParameter: IdentificationParameter
    identificationValue: str
    content: Content