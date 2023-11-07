from typing import Optional

from mapping_sandbox.pydantic import (
    Attributes,
    Company,
    EmployeeOut,
    FilteredModel,
    Id,
    Metadata,
    Value,
    v,
)


class MyModel(FilteredModel):
    greeting: str
    not_set: Optional[str] = None


def test_filtered_model_excludes_none():
    assert "not_set" not in MyModel(greeting="hello").model_dump()


def test_filtered_model_includes_non_none():
    data = MyModel(greeting="hello").model_dump()
    assert "greeting" in data
    assert data["greeting"] == "hello"


def test_value_maps_correctly():
    assert Value[str](value="hello").model_dump() == {"value": "hello"}


def test_id_type_maps_correctly():
    data = Id(type=[v("hello")]).model_dump()
    assert data["type"] == [{"value": "hello"}]


def test_id_id_maps_correctly():
    data = Id(id="012345").model_dump()
    assert data == {"id": "012345"}


def test_company_maps_correctly():
    company = Company(company_code=[v("ACME")])
    assert company.model_dump() == {
        "type": [{"value": ""}],
        "company_code": [{"value": "ACME"}],
    }


def test_company_status_maps_correctly():
    company = Company(company_code=[v("ACME")], status=[v("employed")])
    assert company.model_dump() == {
        "type": [{"value": ""}],
        "company_code": [{"value": "ACME"}],
        "status": [{"value": "employed"}],
    }


def test_attributes_maps_correctly():
    attributes = Attributes(ids=[v(Id(id="1234"))], config_flag=[v(True)])
    assert attributes.model_dump() == {
        "ids": [{"value": {"id": "1234"}}],
        "config_flag": [{"value": True}],
    }


def test_attributes_maps_optional_values_correctly():
    attributes = Attributes(
        first_name="Joe",
        last_name="Smith",
        ids=[],
        config_flag=[],
        company=[v(Company(company_code=[v("ACME")]))],
    )
    assert attributes.model_dump() == {
        "first_name": "Joe",
        "last_name": "Smith",
        "ids": [],
        "config_flag": [],
        "company": [
            {
                "value": {
                    "type": [{"value": ""}],
                    "company_code": [{"value": "ACME"}],
                },
            }
        ],
    }


def test_metadata_maps_correctly():
    metadata = Metadata()
    assert metadata.model_dump() == {"type": "namespace/source/name"}


def test_metadata_maps_optional_values_correctly():
    metadata = Metadata(
        value="test",
        update_date="123456789",
    )
    assert metadata.model_dump() == {
        "type": "namespace/source/name",
        "value": "test",
        "update_date": "123456789",
    }


def test_employee_out_maps_correctly():
    employee_out = EmployeeOut(
        attributes=Attributes(ids=[], config_flag=[]), metadata=[Metadata()]
    )
    assert employee_out.model_dump() == {
        "type": "namespace/employee",
        "attributes": {"ids": [], "config_flag": []},
        "metadata": [{"type": "namespace/source/name"}],
    }
