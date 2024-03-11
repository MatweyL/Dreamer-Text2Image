from datetime import datetime
from typing import Annotated, Any, Optional, List
from uuid import UUID

from pydantic import BaseModel, BeforeValidator

from domain.schemas.core.enums import TaskStatus, FieldTypes


class TaskTypePK(BaseModel):
    uid: UUID

    def __eq__(self, other):
        return self.uid == other.uid

    def __hash__(self):
        return hash(self.uid)


class TaskType(TaskTypePK):
    name: str


class TaskPK(BaseModel):
    uid: UUID


class Task(TaskPK):
    type: TaskTypePK
    status: TaskStatus


class TaskStatusLogPK(BaseModel):
    task_uid: UUID
    created_timestamp: datetime


class TaskStatusLog(TaskStatusLogPK):
    status: TaskStatus
    description: Optional[str] = None


class TaskDataPK(BaseModel):
    uid: UUID


def from_str_to_field_type(value: str):
    return FieldTypes(value)


def from_any_to_str(value: Any):
    return str(value)


class TaskDataBody(BaseModel):
    field_name: str
    field_type: Annotated[FieldTypes, BeforeValidator(from_str_to_field_type)]
    field_value_int: Optional[int] = None
    field_value_float: Optional[float] = None
    field_value_str: Optional[str] = None
    field_value_datetime: Optional[datetime] = None
    is_list: bool

    @property
    def field_value(self):
        if self.field_type == FieldTypes.INT:
            return self.field_value_int
        elif self.field_type == FieldTypes.FLOAT:
            return self.field_value_float
        elif self.field_type == FieldTypes.DATETIME:
            return self.field_value_datetime
        return self.field_value_str


class TaskData(TaskDataPK, TaskDataBody):
    task: TaskPK
    is_input: bool


class FullTask(Task):
    input: Optional[List[TaskData]] = None


class FullTaskStatus(TaskStatusLog):
    output: Optional[List[TaskData]] = None
