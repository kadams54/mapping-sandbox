from typing import Any, Optional, TypeVar

from .base import base_employee
from .schema import Attributes, Company, EmployeeIn, EmployeeOut, Id, Metadata, Value

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
    employee_in = EmployeeIn(**input)

    employee_out = EmployeeOut(**base_employee)
    employee_out.attributes = build_attributes(employee_in)
    employee_out.metadata = build_metadata(employee_in)

    return employee_out.model_dump(exclude_none=True)


def build_attributes(employee_in: EmployeeIn) -> Attributes:
    return Attributes(
        first_name=employee_in.first_name,
        last_name=employee_in.last_name,
        ids=build_ids(employee_in),
        config_flag=[Value[bool](value=False)],
        company=build_company(employee_in),
    )


def build_ids(employee_in: EmployeeIn) -> list[Value[Id]]:
    return [
        Value[Id](value=Id(type=[Value[str](value="hr_id")])),
        Value[Id](value=Id(id=employee_in.employee_number)),
    ]


def build_company(employee_in: EmployeeIn) -> Optional[list[Value[Company]]]:
    if employee_in.company_code is None:
        return None

    company = Company(company_code=[Value[str](value=employee_in.company_code)])

    if employee_in.employment_status is None:
        return [Value[Company](value=company)]

    company.status = [Value[str](value=employee_in.employment_status)]

    return [Value[Company](value=company)]


def build_metadata(employee_in: EmployeeIn) -> list[Metadata]:
    return [
        Metadata(
            update_date=employee_in.event_timestamp, value=employee_in.employee_number
        )
    ]
