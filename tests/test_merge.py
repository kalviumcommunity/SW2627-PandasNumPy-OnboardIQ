import pandas as pd

from src.transformation.merge import (
    aggregate_onboarding,
    aggregate_tool_usage,
    aggregate_support_tickets,
    aggregate_learning,
    merge_employee_data,
)


DATA_PATH = "data/raw"


def load_datasets():
    employee = pd.read_csv(f"{DATA_PATH}/employee.csv")
    onboarding = pd.read_csv(f"{DATA_PATH}/onboarding_progress.csv")
    tool_usage = pd.read_csv(f"{DATA_PATH}/internal_tool_usage.csv")
    support_tickets = pd.read_csv(f"{DATA_PATH}/support_tickets.csv")
    learning = pd.read_csv(f"{DATA_PATH}/learning_management.csv")

    return (
        employee,
        onboarding,
        tool_usage,
        support_tickets,
        learning,
    )


def test_onboarding_aggregation_has_one_row_per_employee():
    _, onboarding, _, _, _ = load_datasets()

    result = aggregate_onboarding(onboarding)

    assert len(result) == 311
    assert result["employee_id"].nunique() == 311
    assert not result["employee_id"].duplicated().any()


def test_tool_usage_aggregation_has_one_row_per_employee():
    _, _, tool_usage, _, _ = load_datasets()

    result = aggregate_tool_usage(tool_usage)

    assert len(result) == 311
    assert result["employee_id"].nunique() == 311
    assert not result["employee_id"].duplicated().any()


def test_support_aggregation_preserves_actual_ticket_coverage():
    _, _, _, support_tickets, _ = load_datasets()

    result = aggregate_support_tickets(support_tickets)

    assert len(result) == 295
    assert result["employee_id"].nunique() == 295
    assert not result["employee_id"].duplicated().any()


def test_learning_aggregation_has_one_row_per_employee():
    _, _, _, _, learning = load_datasets()

    result = aggregate_learning(learning)

    assert len(result) == 311
    assert result["employee_id"].nunique() == 311
    assert not result["employee_id"].duplicated().any()


def test_final_merge_preserves_all_employees():
    (
        employee,
        onboarding,
        tool_usage,
        support_tickets,
        learning,
    ) = load_datasets()

    result = merge_employee_data(
        employee,
        onboarding,
        tool_usage,
        support_tickets,
        learning,
    )

    assert len(result) == 311
    assert result["EmpID"].nunique() == 311
    assert not result["EmpID"].duplicated().any()


def test_final_merge_preserves_employees_without_support_tickets():
    (
        employee,
        onboarding,
        tool_usage,
        support_tickets,
        learning,
    ) = load_datasets()

    result = merge_employee_data(
        employee,
        onboarding,
        tool_usage,
        support_tickets,
        learning,
    )

    assert result["total_support_tickets"].isna().sum() == 16


def test_final_merge_has_no_invalid_employee_references():
    (
        employee,
        onboarding,
        tool_usage,
        support_tickets,
        learning,
    ) = load_datasets()

    employee_ids = set(employee["EmpID"])

    for dataset in [
        onboarding,
        tool_usage,
        support_tickets,
        learning,
    ]:
        assert set(dataset["employee_id"]).issubset(employee_ids)