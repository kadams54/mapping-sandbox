import copy
from functools import partial, reduce
from typing import Any, Callable

from ..base import base_employee


def mapper(input: dict[str, Any]) -> dict[str, Any]:
    """Map the entire object by breaking it up into smaller bits, each
    mapped by its own function. The output object is then piped from
    one mapper function to the next until all the data has been moved
    over. The input object is available because it's been curried. The
    benefits here:

    1. More concise, readable code.
    2. Each function is individually unit-testable.
    3. The pipeline scales. More data means more pipeline steps,
    without increasing cyclomatic complexity.

    The downsides:

    1. Unfamiliar to Python devs. It may take a bit to get oriented
    with what's happening.
    2. Not particularly well-supported in Python, especially when
    compared to languages like OCaml, F#, Clojure, Elixir, Elm, etc.

    Args:
        input (dict[str, Any]): employee info

    Returns:
        dict[str, Any]: employee info in output format
    """
    initial_value = copy.deepcopy(base_employee)

    # Editorial: IF Python had a |> pipe operator, this code would be
    # SO much nicer.
    #
    # return initial_value
    #    |> map_event_timestamp(input)
    #    |> map_employee_number(input)
    #    |> map_first_name(input)
    #    |> map_last_name(input)
    #    |> map_company_code(input)
    #    |> map_employment_status(input)

    return pipeline(
        initial_value,
        [
            map_event_timestamp,
            map_employee_number,
            map_first_name,
            map_last_name,
            map_company_code,
            map_employment_status,
        ],
        args=[input],
    )


def pipeline(
    initial: dict[str, Any],
    funcs: list[Callable],
    args: list[Any] = None,
    kwargs: dict[str, Any] = None,
) -> dict[str, Any]:
    args = args or []
    kwargs = kwargs or {}
    curried_funcs = [partial(f, *args, **kwargs) for f in funcs]
    return reduce(lambda out, f: f(out), curried_funcs, initial)


def map_event_timestamp(
    input: dict[str, Any], output: dict[str, Any]
) -> dict[str, Any]:
    output["metadata"][0]["update_date"] = input["EventTimestamp"]
    return output


def map_employee_number(
    input: dict[str, Any], output: dict[str, Any]
) -> dict[str, Any]:
    output["attributes"]["ids"].append({"value": {"id": input["EmployeeNumber"]}})
    output["metadata"][0]["value"] = input["EmployeeNumber"]
    return output


def map_first_name(input: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    output["attributes"]["first_name"] = input["FirstName"]
    return output


def map_last_name(input: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    output["attributes"]["last_name"] = input["LastName"]
    return output


def map_company_code(input: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    if "CompanyCode" not in input:
        return output
    output["attributes"]["company"] = [
        {
            "value": {
                "type": [{"value": ""}],
                "company_code": [{"value": input["CompanyCode"]}],
            }
        }
    ]
    return output


def map_employment_status(
    input: dict[str, Any], output: dict[str, Any]
) -> dict[str, Any]:
    if "EmploymentStatus" not in input:
        return output
    output["attributes"]["company"][0]["value"]["status"] = [
        {"value": input["EmploymentStatus"]}
    ]
    return output
