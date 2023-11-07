from typing import Any, Callable

import pytest

from mapping_sandbox import (
    with_jinja,
    with_pipeline,
    with_pydantic,
    with_python,
    with_reduce,
)
from mapping_sandbox.base import Mappable

# =====================================================================
# Register all the mappers for testing
# =====================================================================


mappers: list[Mappable] = [
    with_jinja.mapper,
    with_pipeline.mapper,
    with_pydantic.mapper,
    with_python.mapper,
    with_reduce.mapper,
]

# =====================================================================
# The tests: these tests check your mapping implementation.
# =====================================================================


def id_from_fn(val: Any) -> str:
    if isinstance(val, Callable):
        return f"{val.__module__}#{val.__name__}"
    return str(val)


@pytest.mark.parametrize("mapper", mappers, ids=id_from_fn)
def test_map_required_fields(mapper: Mappable):
    assert mapper(
        {
            "EventTimestamp": "2023-11-02T02:15:42.847038",
            "EmployeeNumber": "012345",
            "FirstName": "John",
            "LastName": "McClane",
        }
    ) == {
        "type": "namespace/employee",  # <- from base_output
        "attributes": {
            "first_name": "John",  # <- FirstName
            "last_name": "McClane",  # <- LastName
            "ids": [
                {"value": {"type": [{"value": "hr_id"}]}},  # <- from base_output
                {"value": {"id": "012345"}},  # <- EmployeeNumber
            ],
            "config_flag": [{"value": False}],  # <- from base_output
        },
        "metadata": [
            {
                "type": "namespace/source/name",  # <- from base_output
                "value": "012345",  # <- EmployeeNumber (again)
                "update_date": "2023-11-02T02:15:42.847038",  # <- EventTimestamp
            }
        ],
    }


@pytest.mark.parametrize("mapper", mappers, ids=id_from_fn)
def test_map_optional_fields_all(mapper: Mappable):
    assert mapper(
        {
            "EventTimestamp": "2023-11-02T02:15:42.847038",
            "EmployeeNumber": "054321",
            "FirstName": "Hans",
            "LastName": "Gruber",
            "CompanyCode": "VOLKSFREI",
            "EmploymentStatus": "TERMINATED",
        }
    ) == {
        "type": "namespace/employee",  # <- from base_output
        "attributes": {
            "first_name": "Hans",  # <- FirstName
            "last_name": "Gruber",  # <- LastName
            "ids": [
                {"value": {"type": [{"value": "hr_id"}]}},  # <- from base_output
                {"value": {"id": "054321"}},  # <- EmployeeNumber
            ],
            "config_flag": [{"value": False}],  # <- from base_output
            "company": [
                {
                    "value": {
                        "type": [{"value": ""}],  # <- hard-coded value
                        "company_code": [{"value": "VOLKSFREI"}],  # <- CompanyCode
                        "status": [{"value": "TERMINATED"}],  # <- EmploymentStatus
                    }
                }
            ],
        },
        "metadata": [
            {
                "type": "namespace/source/name",  # <- from base_output
                "value": "054321",  # <- EmployeeNumber (again)
                "update_date": "2023-11-02T02:15:42.847038",  # <- EventTimestamp
            }
        ],
    }


@pytest.mark.parametrize("mapper", mappers, ids=id_from_fn)
def test_map_optional_fields_company_code(mapper: Mappable):
    assert mapper(
        {
            "EventTimestamp": "2023-11-02T02:15:42.847038",
            "EmployeeNumber": "054321",
            "FirstName": "Hans",
            "LastName": "Gruber",
            "CompanyCode": "VOLKSFREI",
        }
    ) == {
        "type": "namespace/employee",  # <- from base_output
        "attributes": {
            "first_name": "Hans",  # <- FirstName
            "last_name": "Gruber",  # <- LastName
            "ids": [
                {"value": {"type": [{"value": "hr_id"}]}},  # <- from base_output
                {"value": {"id": "054321"}},  # <- EmployeeNumber
            ],
            "config_flag": [{"value": False}],  # <- from base_output
            "company": [
                {
                    "value": {
                        "type": [{"value": ""}],  # <- hard-coded value
                        "company_code": [{"value": "VOLKSFREI"}],  # <- CompanyCode
                    }
                }
            ],
        },
        "metadata": [
            {
                "type": "namespace/source/name",  # <- from base_output
                "value": "054321",  # <- EmployeeNumber (again)
                "update_date": "2023-11-02T02:15:42.847038",  # <- EventTimestamp
            }
        ],
    }
