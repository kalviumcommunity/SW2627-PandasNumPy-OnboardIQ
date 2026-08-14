import pandas as pd

from src.preprocessing.cleaning import (
    preprocess_dataset,
    standardize_text_columns,
)


def test_standardize_text_columns():
    df = pd.DataFrame(
        {
            "Department": ["Production   ", " Data Analyst "],
        }
    )

    result = standardize_text_columns(df)

    assert result["Department"].tolist() == [
        "Production",
        "Data Analyst",
    ]


def test_employee_type_standardization():
    df = pd.DataFrame(
        {
            "EmpID": [1, 2],
            "Salary": ["50000", "60000"],
            "Termd": [0, 1],
            "DateofHire": ["2024-01-01", "2023-01-01"],
            "DateofTermination": [None, "2024-01-01"],
        }
    )

    result = preprocess_dataset(df, "employee")

    assert str(result["EmpID"].dtype) == "Int64"
    assert pd.api.types.is_numeric_dtype(result["Salary"])
    assert pd.api.types.is_datetime64_any_dtype(result["DateofHire"])
    assert pd.isna(result.loc[0, "DateofTermination"])


def test_meaningful_nulls_are_preserved():
    df = pd.DataFrame(
        {
            "EmpID": [1],
            "Termd": [0],
            "DateofHire": ["2024-01-01"],
            "DateofTermination": [None],
        }
    )

    result = preprocess_dataset(df, "employee")

    assert pd.isna(result.loc[0, "DateofTermination"])



def test_date_features_are_created():
    df = pd.DataFrame({
        "EmpID": [1],
        "DateofHire": ["2024-01-01"],
        "DateofTermination": ["2024-01-11"],
    })

    result = preprocess_dataset(df, "employee")

    assert pd.api.types.is_datetime64_any_dtype(result["DateofHire"])
    assert result.loc[0, "tenure_days"] == 10


def test_iqr_outlier_is_flagged_without_removing_rows():
    df = pd.DataFrame({
        "EmpID": [1, 2, 3, 4, 5],
        "Salary": [50000, 51000, 52000, 53000, 200000],
        "DateofHire": ["2024-01-01"] * 5,
        "DateofTermination": [None] * 5,
    })

    result = preprocess_dataset(df, "employee")

    assert len(result) == 5
    assert bool(result.loc[4, "Salary_outlier"]) is True
    assert bool(result.loc[0, "Salary_outlier"]) is False
def test_onboarding_features():
    from src.features.business_features import calculate_onboarding_features

    df = pd.DataFrame({
        "employee_id": [1, 1, 2],
        "task_status": ["Completed", "Pending", "Completed"],
    })

    result = calculate_onboarding_features(df)

    assert result.loc[
        result["employee_id"] == 1,
        "total_onboarding_tasks"
    ].iloc[0] == 2

    assert result.loc[
        result["employee_id"] == 1,
        "onboarding_completion_percentage"
    ].iloc[0] == 50


def test_support_ticket_features():
    from src.features.business_features import calculate_support_features

    df = pd.DataFrame({
        "employee_id": [1, 1, 2],
    })

    result = calculate_support_features(df)

    assert result.loc[
        result["employee_id"] == 1,
        "support_ticket_count"
    ].iloc[0] == 2


def test_learning_features():
    from src.features.business_features import calculate_learning_features

    df = pd.DataFrame({
        "employee_id": [1, 1, 2],
        "course_status": ["Completed", "Pending", "Completed"],
    })

    result = calculate_learning_features(df)

    assert result.loc[
        result["employee_id"] == 1,
        "learning_completion_rate"
    ].iloc[0] == 50


def test_first_week_activity():
    from src.features.business_features import calculate_first_week_activity

    employee = pd.DataFrame({
        "EmpID": [1],
        "DateofHire": ["2024-01-01"],
    })

    usage = pd.DataFrame({
        "employee_id": [1, 1],
        "usage_date": ["2024-01-02", "2024-01-10"],
        "slack_activity_count": [5, 10],
        "jira_usage_count": [2, 5],
    })

    result = calculate_first_week_activity(usage, employee)

    assert result.loc[0, "first_week_activity"] == 7
def test_productivity_indicator():
    from src.features.business_features import calculate_productivity_indicator

    df = pd.DataFrame({
        "employee_id": [1],
        "onboarding_completion_percentage": [80],
        "learning_completion_rate": [90],
        "first_week_activity": [10],
    })

    result = calculate_productivity_indicator(df)

    assert result.loc[0, "productivity_indicator"] == 180
