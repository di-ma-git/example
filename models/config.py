from pydantic import BaseModel


class Envs(BaseModel):
    db_host: str
    db_port: str
    db_user: str
    db_pass: str
    db_name: str


class Urls(BaseModel):
    base_url_dev: str
    base_url_test: str
    create_task: str
    create_task_v2: str
    create_task_v3: str
    search_v1: str
    search_v2: str
    search_v3_one_part: str
    search_v3_two_part: str
    search_v4: str
    upload: str
    provide: str