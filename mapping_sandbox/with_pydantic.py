from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, model_serializer
from pydantic.alias_generators import to_pascal

T = TypeVar("T")


def mapper(input: dict[str, Any]) -> dict[str, Any]:
    """This mapper uses Pydantic to build up at least one and possibly two
    models of the data.  Even though Pydantic doesn't solve the mapping issue
    for us, using the models does get us more validation and type checking on
    potentially unsafe data. It also lends itself, depending on the approach
    taken, to mapping in smaller chunks, which is, in turn, more easily unit
    testable.

    Args:
        input (dict[str, Any]): employee info

    Returns:
        dict[str, Any]: employee info in output format
    """
    employee = Employee(**input)

    attributes = Attributes(
        first_name=employee.first_name,
        last_name=employee.last_name,
        ids=[
            Value[Id](value=Id(type=[Value[str](value="hr_id")])),
            Value[Id](value=Id(id=employee.employee_number)),
        ],
        config_flag=[Value[bool](value=False)],
    )
    if employee.company_code is not None:
        attributes.company = [
            Value[Company](
                value=Company(company_code=[Value[str](value=employee.company_code)])
            )
        ]
        if employee.employment_status is not None:
            attributes.company[0].value.status = [
                Value[str](value=employee.employment_status)
            ]

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


def v(value: T) -> Value[T]:
    return Value[T](value=value)


class FilteredModel(BaseModel):
    @model_serializer
    def ser_model(self) -> dict[str, Any]:
        return {k: v for k, v in dict(self).items() if v is not None}


class Id(FilteredModel):
    type: Optional[list[Value[str]]] = None
    id: Optional[str] = None


class Company(FilteredModel):
    type: list[Value[str]] = [Value[str](value="")]
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
