from typing import Any

from .base import base_employee
from .functools import pipeline
from .schema import Attributes, Company, EmployeeIn, EmployeeOut, Id, Metadata, Value


def mapper(input: dict[str, Any]) -> dict[str, Any]:
    """This mapper uses Pydantic to build up at least one and possibly two
    models of the data.  Even though Pydantic doesn't solve the mapping issue
    for us, using the models does get us more validation and type checking on
    potentially unsafe data. It also lends itself, depending on the approach
    taken, to mapping in smaller chunks, which is, in turn, more easily unit
    testable.

    Additionally we're testing two-way serialization here, so there are actually
    two mapping functions in this implementation.

    Obligatory editorial: this is what this function could look like with a pipe
    operator (|>):

    employee = Employee(**input)
    return {}
        |> map_attributes(employee)
        |> map_company_code(employee)
        |> map_employment_status(employee)
        |> map_metadata(employee)
        |> dumps

    Args:
        input (dict[str, Any]): employee info

    Returns:
        dict[str, Any]: employee info in output format
    """
    employee_in = EmployeeIn(**input)

    employee_out = pipeline(
        EmployeeOut(**base_employee),
        [
            map_attributes,
            map_company_code,
            map_employment_status,
            map_metadata,
        ],
        curried_args=[employee_in],
    )

    return employee_out.model_dump(exclude_none=True)


def map_attributes(employee_out: EmployeeOut, employee_in: EmployeeIn) -> EmployeeOut:
    employee_out.attributes = Attributes(
        first_name=employee_in.first_name,
        last_name=employee_in.last_name,
        ids=[
            Value[Id](value=Id(type=[Value[str](value="hr_id")])),
            Value[Id](value=Id(id=employee_in.employee_number)),
        ],
        config_flag=[Value[bool](value=False)],
    )
    return employee_out


def map_company_code(employee_out: EmployeeOut, employee_in: EmployeeIn) -> EmployeeOut:
    if employee_in.company_code is None:
        return employee_out

    employee_out.attributes.company = [
        Value[Company](
            value=Company(company_code=[Value[str](value=employee_in.company_code)])
        )
    ]
    return employee_out


def map_employment_status(
    employee_out: EmployeeOut, employee_in: EmployeeIn
) -> EmployeeOut:
    if employee_in.company_code is None or employee_in.employment_status is None:
        return employee_out
    if employee_out.attributes.company is None:
        return employee_out

    employee_out.attributes.company[0].value.status = [
        Value[str](value=employee_in.employment_status)
    ]
    return employee_out


def map_metadata(employee_out: EmployeeOut, employee_in: EmployeeIn) -> EmployeeOut:
    employee_out.metadata = [
        Metadata(
            value=employee_in.employee_number,
            update_date=employee_in.event_timestamp,
        )
    ]
    return employee_out
