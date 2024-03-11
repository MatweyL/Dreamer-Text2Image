from typing import Type

from pydantic import BaseModel

from ports.common import ConverterI


class StrToPydantic(ConverterI):

    def __init__(self, schema: Type[BaseModel]):
        self._schema = schema

    def convert(self, data: str) -> Type[BaseModel]:
        return self._schema.model_validate_json(data)
