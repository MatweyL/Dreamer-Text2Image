from datetime import datetime
from functools import partial
from typing import List, Type
from uuid import UUID, uuid4

from pydantic import BaseModel

from domain.schemas.core.enums import FieldTypes
from domain.schemas.core.task import TaskData, TaskPK


class TaskDataConverter:

    def to_schema(self, task_datas: List[TaskData], schema: Type[BaseModel]) -> Type[BaseModel]:
        task_datas_dict = {}
        for task_data in task_datas:
            if task_data.is_list:
                try:
                    task_datas_dict[task_data.field_name].append(task_data.field_value)
                except KeyError:
                    task_datas_dict[task_data.field_name] = [task_data.field_value]
            else:
                task_datas_dict[task_data.field_name] = task_data.field_value
        return schema(**task_datas_dict)

    def to_data(self, task: TaskPK, is_input: bool, **variables) -> List[TaskData]:
        task_datas = []
        for name, value in variables.items():
            if isinstance(value, list):
                for list_value in value:
                    task_datas.append(self.variable_to_data(task, name, list_value, True, is_input))
            else:
                task_datas.append(self.variable_to_data(task, name, value, False, is_input))
        return task_datas

    def variable_to_data(self, task: TaskPK, name: str, value, is_list: bool,
                         is_input: bool, uid: UUID = None) -> TaskData:
        if not uid:
            uid = uuid4()
        task_data_builder = partial(TaskData, task=task, is_input=is_input, is_list=is_list, field_name=name, uid=uid)
        if isinstance(value, datetime):
            return task_data_builder(field_value_datetime=value, field_type=FieldTypes.DATETIME)
        elif isinstance(value, str):
            return task_data_builder(field_value_str=value, field_type=FieldTypes.STRING)
        elif isinstance(value, int):
            return task_data_builder(field_value_int=value, field_type=FieldTypes.INT)
        elif isinstance(value, float):
            return task_data_builder(field_value_float=value, field_type=FieldTypes.FLOAT)
        raise RuntimeError(f'unknown field type ({type(value)}): {value}')
