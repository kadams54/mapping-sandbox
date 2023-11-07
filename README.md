# Mapping Fun

Mapping from one JSON format to another is often soul-sucking, yet-necessary work in integrating modern APIs together. This playground provides a place to play around with different approaches to this problem in a Python environment.

# The Problem

Convert JSON input data (as a dict) to JSON output data (also a dict).

**Input:**

```python
{
    "EventTimestamp": "2023-11-02T02:15:42.847038",
    "EmployeeNumber": "012345",
    "FirstName": "John",
    "LastName": "McClane",
}
```
**Output:**

```python
{
    "type": "foo/bar",  # <- hard-coded value
    "attributes": {
        "first_name": "John",  # <- FirstName
        "last_name": "McClane",  # <- LastName
        "ids": [
            {"value": {"type": [{"value": "hr_id"}]}},  # <- hard-coded value
            {"value": {"id": "012345"}},  # <- EmployeeNumber
        ],
        "config_flag": [{"value": False}],  # <- hard-coded value
    },
    "metadata": [
        {
            "type": "namespace/source/name",  # <- hard-coded value
            "value": "012345",  # <- EmployeeNumber (again)
            "update_date": "2023-11-02T02:15:42.847038",  # <- EventTimestamp
        }
    ],
}
```

## A Twist

There are two optional fields: `CompanyCode` and `EmploymentStatus`. If they are not present in the input, then their corresponding fields should not be present in the output. It's possible to have `CompanyCode` without `EmploymentStatus` but not the other way around; `EmploymentStatus` will _always_ have a `CompanyCode`.

**Input:**

```python
{
    "EventTimestamp": "2023-11-02T02:15:42.847038",
    "EmployeeNumber": "054321",
    "FirstName": "Hans",
    "LastName": "Gruber",
    "CompanyCode": "VOLKSFREI",
    "EmploymentStatus": "TERMINATED",
}
```

**Output:**

```python
{
    "type": "foo/bar",  # <- hard-coded value
    "attributes": {
        "first_name": "Hans",  # <- FirstName
        "last_name": "Gruber",  # <- LastName
        "ids": [
            {"value": {"type": [{"value": "hr_id"}]}},  # <- hard-coded value
            {"value": {"id": "054321"}},  # <- EmployeeNumber
        ],
        "config_flag": [{"value": False}],  # <- hard-coded value
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
            "type": "namespace/source/name",  # <- hard-coded value
            "value": "054321",  # <- EmployeeNumber (again)
            "update_date": "2023-11-02T02:15:42.847038",  # <- EventTimestamp
        }
    ],
}
```

# How to Play

## Prerequisites

- Python >= 3.9 as things like dataclasses (3.7), `TypedDict` (3.8), and generics in standard collections (3.9) are leveraged pretty heavily in this problem space.
- [Poetry](https://python-poetry.org/)

## Getting started

```sh
poetry install
```

## Playing with mappers

1. Add a `with_*.py` file for a new mapper implementation or modify one of the existing mappers.
1. Register any new mappers in the `tests/test-end-to-end.py` file by adding them to the `mappers` list.

The only requirement for a mapper: it must take in a `dict[str, Any]` and returns a `dict[str, Any]`.

## Available tools

There are a number of dev tools available to make it easier to play around with various mapping implementations:

- [Python devtools](https://python-devtools.helpmanual.io/) - use `debug()` to help troubleshoot why a particular mapping isn't working
- [rich](https://github.com/Textualize/rich) - similar to the above, a better `print()` when playing in the REPL
- [ptpython](https://github.com/prompt-toolkit/ptpython) - speaking of REPLs, upgrade your standard Python REPL with `ptpython`
- [pytest-sugar](https://github.com/Teemu/pytest-sugar) - nicer build output

Also: the project leverages the following dev tools:

- [ruff](https://docs.astral.sh/ruff/) for linting
- [black](https://black.readthedocs.io/en/stable/) for formatting
- [mypy](https://github.com/python/mypy) for type checking

If you're using VS Code and have the associated extensions installed, they should work out of the box. Other code editors may need a little more configuration.