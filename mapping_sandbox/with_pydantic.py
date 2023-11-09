from typing import Any

from .schema import Attributes, Company, EmployeeIn, EmployeeOut, Id, Metadata, Value


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

    attributes = Attributes(
        first_name=employee_in.first_name,
        last_name=employee_in.last_name,
        ids=[
            Value[Id](value=Id(type=[Value[str](value="hr_id")])),
            Value[Id](value=Id(id=employee_in.employee_number)),
        ],
        config_flag=[Value[bool](value=False)],
    )
    if employee_in.company_code is not None:
        attributes.company = [
            Value[Company](
                value=Company(company_code=[Value[str](value=employee_in.company_code)])
            )
        ]
        if employee_in.employment_status is not None:
            attributes.company[0].value.status = [
                Value[str](value=employee_in.employment_status)
            ]

    employee_out = EmployeeOut(
        attributes=attributes,
        metadata=[
            Metadata(
                value=employee_in.employee_number,
                update_date=employee_in.event_timestamp,
            )
        ],
    )

    return employee_out.model_dump(exclude_none=True)
