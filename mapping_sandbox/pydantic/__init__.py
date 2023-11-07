from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, model_serializer
from pydantic.alias_generators import to_pascal

T = TypeVar("T")


def mapper(input: dict[str, Any]) -> dict[str, Any]:
    employee = Employee(**input)

    attributes = Attributes(
        first_name=employee.first_name,
        last_name=employee.last_name,
        ids=[
            v(Id(type=[v("hr_id")])),
            v(Id(id=employee.employee_number)),
        ],
        config_flag=[v(False)],
    )
    if employee.company_code is not None:
        attributes.company = [v(Company(company_code=[v(employee.company_code)]))]
        if employee.employment_status is not None:
            attributes.company[0]["value"].status = [v(employee.employment_status)]

    employee_out = EmployeeOut(
        attributes=attributes,
        metadata=[
            Metadata(
                value=employee.employee_number,
                update_date=employee.event_timestamp,
            )
        ],
    )

    return employee_out.model_dump()


class Employee(BaseModel):
    model_config = ConfigDict(alias_generator=to_pascal)

    event_timestamp: str
    employee_number: str
    first_name: str
    last_name: str
    company_code: Optional[str] = None
    employment_status: Optional[str] = None


class Value(BaseModel, Generic[T]):
    value: T


def v(value: T) -> dict[str, T]:
    return {"value": value}


class FilteredModel(BaseModel):
    @model_serializer
    def ser_model(self) -> dict[str, Any]:
        return {k: v for k, v in dict(self).items() if v is not None}


class Id(FilteredModel):
    type: Optional[list[Value[str]]] = None
    id: Optional[str] = None


class Company(FilteredModel):
    type: list[Value[str]] = [v("")]
    company_code: list[Value[str]]
    status: Optional[list[Value[str]]] = None


class Attributes(FilteredModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    ids: list[Value[Id]]
    config_flag: list[Value[bool]]
    company: Optional[list[Value[Company]]] = None


class Metadata(FilteredModel):
    type: str = "namespace/source/name"
    value: Optional[str] = None
    update_date: Optional[str] = None


class EmployeeOut(FilteredModel):
    type: str = "namespace/employee"
    attributes: Attributes
    metadata: list[Metadata]
