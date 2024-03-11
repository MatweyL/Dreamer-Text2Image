import pprint
from datetime import datetime
from typing import List
from uuid import uuid4

import pytest
from pydantic import BaseModel

from domain.schemas.core.enums import FieldTypes
from domain.schemas.core.task import TaskPK, TaskData
from domain.task_data_converter import TaskDataConverter


class TestSchema(BaseModel):
    int_val: int
    datetime_val: datetime
    str_vals: List[str]


def test_to_schema_converting():
    task_data_converter = TaskDataConverter()
    task_pk = TaskPK(uid=uuid4())
    is_input = True
    task_datas = [TaskData(task=task_pk, is_input=is_input, field_name='int_val', uid=uuid4(),
                           field_value_int=1, field_type=FieldTypes.INT, is_list=False),
                  TaskData(task=task_pk, is_input=is_input, field_name='datetime_val', uid=uuid4(),
                           field_value_datetime=datetime.now(), field_type=FieldTypes.DATETIME, is_list=False),
                  TaskData(task=task_pk, is_input=is_input, field_name='str_vals', uid=uuid4(),
                           field_value_str='a', field_type=FieldTypes.STRING, is_list=True),
                  TaskData(task=task_pk, is_input=is_input, field_name='str_vals', uid=uuid4(),
                           field_value_str='b', field_type=FieldTypes.STRING, is_list=True),
                  TaskData(task=task_pk, is_input=is_input, field_name='str_vals', uid=uuid4(),
                           field_value_str='c', field_type=FieldTypes.STRING, is_list=True),
                  ]
    ts: TestSchema = task_data_converter.to_schema(task_datas, TestSchema)
    pprint.pprint(ts.model_dump())


def test_variable_to_data():
    task_data_converter = TaskDataConverter()
    task_pk = TaskPK(uid=uuid4())
    is_list = False
    is_input = True
    td = task_data_converter.variable_to_data(task_pk, 'a', 1, is_list, is_input)
    assert td.field_name == 'a'
    assert td.field_value == 1
    assert td.is_list == is_list
    assert td.is_input == is_input


def test_to_data():
    task_data_converter = TaskDataConverter()
    task_pk = TaskPK(uid=uuid4())
    is_input = True
    variables = dict(int_val=1, datetime_val=datetime.now(), str_vals=['str1', 'str2', 'str3'])
    task_datas = task_data_converter.to_data(task_pk, is_input, **variables)
