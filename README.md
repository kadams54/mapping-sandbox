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

`main.py` has everything you need. At the bottom of the file are the tests, which will run when you run this project. In the space indicated, you can add whatever functions you need in order to make those tests pass.

The only requirement is that you have a top-level, or entrypoint function that takes in a `dict[str, Any]` and returns a `dict[str, Any]`. Once you have that top-level function, you can add it to the `mappers` list so that it's included in the tests. The `mappers` list lets us test multiple implementations at once.

I've included a `map_with_pure_python` implementation as an example and starter function.