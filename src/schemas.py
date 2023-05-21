from datetime import datetime
from typing import Any, Callable
from zoneinfo import ZoneInfo

import orjson
from pydantic import BaseModel as PydanticBaseModel
from pydantic import root_validator


def orjson_dumps(v: Any, *, default: Callable[[Any], Any] | None) -> str:
    return orjson.dumps(v, default=default).decode()


def to_camel(string: str) -> str:
    return string.split("_")[0] + "".join(
        word.capitalize() for word in string.split("_")[1:]
    )


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class BaseModel(PydanticBaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {datetime: convert_datetime_to_gmt}
        allow_population_by_field_name = True
        alias_generator = to_camel

        @staticmethod
        def schema_extra(schema: dict):
            """
            This makes sure the field which hidden attribute is set to True will not appear in the Swagger UI docs.
            """
            props = {}
            for k, v in schema.get("properties", {}).items():
                if not v.get("hidden", False):
                    props[k] = v
            schema["properties"] = props

    @root_validator()
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}


class Message(PydanticBaseModel):
    detail: str
