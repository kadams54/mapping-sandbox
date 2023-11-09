from hypothesis import given
from hypothesis.strategies import builds, text

from mapping_sandbox.schema import EmployeeIn
from mapping_sandbox.with_pydantic_builder import (
    build_attributes,
    build_company,
    build_ids,
    build_metadata,
)


@given(builds(EmployeeIn))
def test_build_attributes(employee_in: EmployeeIn):
    model = build_attributes(employee_in)
    assert model.first_name == employee_in.first_name
    assert model.last_name == employee_in.last_name
    assert len(model.config_flag) > 0
    assert model.config_flag[0].value is False


@given(builds(EmployeeIn))
def test_build_ids(employee_in: EmployeeIn):
    model_list = build_ids(employee_in)
    assert len(model_list) == 2
    id_type = model_list[0].value.type
    assert id_type is not None
    assert len(id_type) > 0
    assert id_type[0].value == "hr_id"
    id = model_list[1].value.id
    assert id == employee_in.employee_number


@given(builds(EmployeeIn, CompanyCode=text()))
def test_build_company(employee_in: EmployeeIn):
    model_list = build_company(employee_in)
    assert model_list is not None
    assert len(model_list) > 0
    company = model_list[0].value
    assert len(company.company_code) > 0
    assert company.company_code[0].value == employee_in.company_code


@given(builds(EmployeeIn, CompanyCode=text(), EmploymentStatus=text()))
def test_build_company_with_employment_status(employee_in: EmployeeIn):
    model_list = build_company(employee_in)
    assert model_list is not None
    assert len(model_list) > 0
    company = model_list[0].value
    assert company.status is not None
    assert len(company.status) > 0
    assert company.status[0].value == employee_in.employment_status


@given(builds(EmployeeIn))
def test_build_metadata(employee_in: EmployeeIn):
    model_list = build_metadata(employee_in)
    assert len(model_list) > 0
    metadata = model_list[0]
    assert metadata.update_date == employee_in.event_timestamp
    assert metadata.value == employee_in.employee_number
