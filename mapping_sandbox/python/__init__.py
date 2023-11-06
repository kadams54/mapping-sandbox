import copy
from typing import Any

from ..base import base_employee


def mapper(input: dict[str, Any]) -> dict[str, Any]:
    """Straight forward, vanilla Python implementation. This approach
    has two problems:

    1. It can't be broken up and unit tested in chunks, e.g., validate
    that the employee first_name field was mapped correctly independent
    from any other fields.
    2. It doesn't scale. As more fields need to be mapped into
    increasingly complex data structures, the cyclomatic complexity of
    the function also goes up due to the proliferation of if/else
    statements.

    Args:
        input (dict[str, Any]): employee info

    Returns:
        dict[str, Any]: employee info in output format
    """
    output = copy.deepcopy(base_employee)

    # Required fields.
    output["metadata"][0]["update_date"] = input["EventTimestamp"]
    output["metadata"][0]["value"] = input["EmployeeNumber"]
    output["attributes"]["first_name"] = input["FirstName"]
    output["attributes"]["last_name"] = input["LastName"]
    output["attributes"]["ids"].append({"value": {"id": input["EmployeeNumber"]}})

    # Optional fields.
    if "CompanyCode" in input:
        output["attributes"]["company"] = [
            {
                "value": {
                    "type": [{"value": ""}],
                    "company_code": [{"value": input["CompanyCode"]}],
                }
            }
        ]
        if "EmploymentStatus" in input:
            output["attributes"]["company"][0]["value"]["status"] = [
                {"value": input["EmploymentStatus"]}
            ]

    return output
