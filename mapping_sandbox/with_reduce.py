import copy
from functools import reduce
from typing import Any

from .base import base_employee


def mapper(input: dict[str, Any]) -> dict[str, Any]:
    """This approach uses reduce + pattern matching to build the
    employee output. It also suffers from the same two issues in the
    vanilla Python approach; however, we're starting to see field-
    specific logic emerging in each case. These blocks of logic could
    be organized into their own functions and unit tested. That said,
    the unit tests would still need to know a great deal about the
    convoluted output data structure.

    Args:
        input (dict[str, Any]): employee info

    Returns:
        dict[str, Any]: employee info in output format
    """
    output = copy.deepcopy(base_employee)
    return reduce(build_employee, input.items(), output)


def build_employee(output: dict[str, Any], item: tuple[str, Any]) -> dict[str, Any]:
    match item:
        case ("EventTimestamp", event_timestamp):
            output["metadata"][0]["update_date"] = event_timestamp
        case ("EmployeeNumber", employee_number):
            output["attributes"]["ids"].append({"value": {"id": employee_number}})
            output["metadata"][0]["value"] = employee_number
        case ("FirstName", first_name):
            output["attributes"]["first_name"] = first_name
        case ("LastName", last_name):
            output["attributes"]["last_name"] = last_name
        case ("CompanyCode", company_code):
            output["attributes"]["company"] = [
                {
                    "value": {
                        "type": [{"value": ""}],
                        "company_code": [{"value": company_code}],
                    }
                }
            ]
        case ("EmploymentStatus", employment_status):
            output["attributes"]["company"][0]["value"]["status"] = [
                {"value": employment_status}
            ]
        case _:
            pass
    return output
