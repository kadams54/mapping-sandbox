import copy
from functools import reduce
from typing import Any

from .base import base_employee


def mapper(input: dict[str, Any]) -> dict[str, Any]:
    """This approach uses reduce to build the employee output. It also suffers
    from the same two issues in the vanilla Python approach; however, we're
    starting to see field- specific logic emerging in each case. These blocks of
    logic could be organized into their own functions and unit tested. That
    said, the unit tests would still need to know a great deal about the
    convoluted output data structure.

    Args:
        input (dict[str, Any]): employee info

    Returns:
        dict[str, Any]: employee info in output format
    """
    output = copy.deepcopy(base_employee)
    return reduce(build_employee, input.items(), output)


def build_employee(output: dict[str, Any], item: tuple[str, Any]) -> dict[str, Any]:
    key, value = item
    if key == "EventTimestamp":
        output["metadata"][0]["update_date"] = value
    elif key == "EmployeeNumber":
        output["attributes"]["ids"].append({"value": {"id": value}})
        output["metadata"][0]["value"] = value
    elif key == "FirstName":
        output["attributes"]["first_name"] = value
    elif key == "LastName":
        output["attributes"]["last_name"] = value
    elif key == "CompanyCode":
        output["attributes"]["company"] = [
            {
                "value": {
                    "type": [{"value": ""}],
                    "company_code": [{"value": value}],
                }
            }
        ]
    elif key == "EmploymentStatus":
        output["attributes"]["company"][0]["value"]["status"] = [{"value": value}]
    else:
        pass
    return output
