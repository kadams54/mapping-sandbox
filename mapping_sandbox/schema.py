from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal

T = TypeVar("T")


class EmployeeIn(BaseModel):
    model_config = ConfigDict(alias_generator=to_pascal)

    event_timestamp: str
    employee_number: str
    first_name: str
    last_name: str
    company_code: Optional[str] = None
    employment_status: Optional[str] = None


class Value(BaseModel, Generic[T]):
    value: T


class Id(BaseModel):
    type: Optional[list[Value[str]]] = None
    id: Optional[str] = None


class Company(BaseModel):
    type: list[Value[str]] = [Value[str](value="")]
    company_code: list[Value[str]]
    status: Optional[list[Value[str]]] = None


class Attributes(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    ids: list[Value[Id]]
    config_flag: list[Value[bool]]
    company: Optional[list[Value[Company]]] = None


class Metadata(BaseModel):
    type: str = "namespace/source/name"
    value: Optional[str] = None
    update_date: Optional[str] = None


class EmployeeOut(BaseModel):
    type: str = "namespace/employee"
    attributes: Attributes
    metadata: list[Metadata]
