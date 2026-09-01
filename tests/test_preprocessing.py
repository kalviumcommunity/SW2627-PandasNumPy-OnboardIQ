import pandas as pd
import pytest

from src.features.business_features import (
    calculate_first_week_activity,
    calculate_learning_features,
    calculate_onboarding_features,
    calculate_productivity_indicator,
    calculate_support_features,
)
from src.preprocessing.cleaning import (
    convert_data_types,
    detect_iqr_outliers,
    handle_missing_values,
    preprocess_dataset,
    remove_duplicate_rows,
    standardize_text_columns,
    validate_processed_data,
)


def test_standardize_text_columns():
    df = pd.DataFrame(
        {
            "Department": [
                "Production   ",
                " Data Analyst ",
            ],
        }
    )

    result = standardize_text_columns(df)

    assert result["Department"].tolist() == [
        "Production",
        "Data Analyst",
    ]


def test_standardize_internal_whitespace():
    df = pd.DataFrame(
        {
            "Department": [
                "Production       ",
                "Software    Engineering",
            ],
        }
    )

    result = standardize_text_columns(df)

    assert result["Department"].tolist() == [
        "Production",
        "Software Engineering",
    ]


def test_remove_duplicate_rows():
    df = pd.DataFrame(
        {
            "EmpID": [1, 1, 2],
            "Department": [
                "Production",
                "Production",
                "Sales",
            ],
        }
    )

    result = remove_duplicate_rows(df)

    assert len(result) == 2
    assert result["EmpID"].tolist() == [1, 2]


def test_preprocess_removes_duplicate_rows():
    df = pd.DataFrame(
        {
            "EmpID": [1, 1],
            "Salary": [50000, 50000],
            "Termd": [0, 0],
            "DateofHire": [
                "2024-01-01",
                "2024-01-01",
            ],
            "DateofTermination": [
                None,
                None,
            ],
        }
    )

    result = preprocess_dataset(df, "employee")

    assert len(result) == 1


def test_employee_type_standardization():
    df = pd.DataFrame(
        {
            "EmpID": [1, 2],
            "Salary": ["50000", "60000"],
            "Termd": [0, 1],
            "DateofHire": [
                "2024-01-01",
                "2023-01-01",
            ],
            "DateofTermination": [
                None,
                "2024-01-01",
            ],
        }
    )

    result = preprocess_dataset(df, "employee")

    assert str(result["EmpID"].dtype) == "Int64"
    assert pd.api.types.is_numeric_dtype(result["Salary"])
    assert pd.api.types.is_datetime64_any_dtype(
        result["DateofHire"]
    )
    assert pd.isna(result.loc[0, "DateofTermination"])


def test_convert_data_types_handles_invalid_values():
    df = pd.DataFrame(
        {
            "EmpID": ["1", "invalid"],
            "Salary": ["50000", "invalid"],
            "DateofHire": [
                "2024-01-01",
                "invalid-date",
            ],
        }
    )

    schema = {
        "integer": ["EmpID"],
        "numeric": ["Salary"],
        "datetime": ["DateofHire"],
        "text": [],
    }

    result = convert_data_types(df, schema)

    assert str(result["EmpID"].dtype) == "Int64"
    assert pd.isna(result.loc[1, "EmpID"])

    assert pd.api.types.is_numeric_dtype(result["Salary"])
    assert pd.isna(result.loc[1, "Salary"])

    assert pd.api.types.is_datetime64_any_dtype(
        result["DateofHire"]
    )
    assert pd.isna(result.loc[1, "DateofHire"])


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


def test_handle_missing_values_preserves_nulls():
    df = pd.DataFrame(
        {
            "EmpID": [1, 2],
            "DateofTermination": [
                pd.NaT,
                pd.Timestamp("2024-01-10"),
            ],
            "completion_time_hours": [
                pd.NA,
                5,
            ],
        }
    )

    result = handle_missing_values(df)

    assert pd.isna(result.loc[0, "DateofTermination"])
    assert pd.isna(result.loc[0, "completion_time_hours"])


def test_employee_tenure_feature_is_created():
    df = pd.DataFrame(
        {
            "EmpID": [1],
            "DateofHire": ["2024-01-01"],
            "DateofTermination": ["2024-01-11"],
        }
    )

    result = preprocess_dataset(df, "employee")

    assert pd.api.types.is_datetime64_any_dtype(
        result["DateofHire"]
    )
    assert result.loc[0, "tenure_days"] == 10


def test_active_employee_tenure_is_calculated():
    df = pd.DataFrame(
        {
            "EmpID": [1],
            "DateofHire": ["2024-01-01"],
            "DateofTermination": [None],
        }
    )

    result = preprocess_dataset(df, "employee")

    assert "tenure_days" in result.columns
    assert result.loc[0, "tenure_days"] >= 0


def test_onboarding_days_overdue_feature_is_created():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2],
            "onboarding_task_id": ["T1", "T2"],
            "task_name": ["Task 1", "Task 2"],
            "task_category": ["Admin", "Technical"],
            "current_stage": ["Complete", "Complete"],
            "task_status": ["Completed", "Completed"],
            "completion_percentage": [100, 100],
            "due_date": [
                "2024-01-01",
                "2024-01-10",
            ],
            "completed_date": [
                "2024-01-05",
                "2024-01-08",
            ],
        }
    )

    result = preprocess_dataset(
        df,
        "onboarding_progress",
    )

    assert "days_overdue" in result.columns
    assert result.loc[0, "days_overdue"] == 4
    assert result.loc[1, "days_overdue"] == 0


def test_learning_duration_feature_is_created():
    df = pd.DataFrame(
        {
            "employee_id": [1],
            "learning_record_id": ["L1"],
            "course_name": ["Python"],
            "course_type": ["Technical"],
            "course_status": ["Completed"],
            "assessment_score": [90],
            "completion_time_hours": [5],
            "assigned_date": ["2024-01-01"],
            "completed_date": ["2024-01-04"],
        }
    )

    result = preprocess_dataset(
        df,
        "learning_management",
    )

    assert "learning_duration_days" in result.columns
    assert result.loc[0, "learning_duration_days"] == 3


def test_iqr_outlier_is_flagged_without_removing_rows():
    df = pd.DataFrame(
        {
            "EmpID": [1, 2, 3, 4, 5],
            "Salary": [
                50000,
                51000,
                52000,
                53000,
                200000,
            ],
            "DateofHire": ["2024-01-01"] * 5,
            "DateofTermination": [None] * 5,
        }
    )

    result = preprocess_dataset(df, "employee")

    assert len(result) == 5
    assert bool(result.loc[4, "Salary_outlier"]) is True
    assert bool(result.loc[0, "Salary_outlier"]) is False


def test_detect_iqr_outliers_skips_missing_columns():
    df = pd.DataFrame(
        {
            "Salary": [50000, 51000, 52000],
        }
    )

    result = detect_iqr_outliers(
        df,
        ["Salary", "NonExistentColumn"],
    )

    assert "Salary_outlier" in result.columns
    assert "NonExistentColumn_outlier" not in result.columns
    assert len(result) == 3


def test_outlier_detection_does_not_remove_rows():
    df = pd.DataFrame(
        {
            "Salary": [
                50000,
                51000,
                52000,
                53000,
                200000,
            ],
        }
    )

    result = detect_iqr_outliers(
        df,
        ["Salary"],
    )

    assert len(result) == len(df)
    assert "Salary_outlier" in result.columns


def test_validate_processed_data_rejects_duplicate_primary_keys():
    df = pd.DataFrame(
        {
            "EmpID": [1, 1],
        }
    )

    with pytest.raises(
        ValueError,
        match="duplicate primary keys",
    ):
        validate_processed_data(
            df,
            "employee",
        )


def test_validate_processed_data_rejects_null_primary_key():
    df = pd.DataFrame(
        {
            "EmpID": pd.Series(
                [1, None],
                dtype="Int64",
            ),
        }
    )

    with pytest.raises(
        ValueError,
        match="contains nulls",
    ):
        validate_processed_data(
            df,
            "employee",
        )


def test_validate_processed_data_rejects_invalid_completion_percentage():
    df = pd.DataFrame(
        {
            "employee_id": [1],
            "onboarding_task_id": ["T1"],
            "completion_percentage": [150],
        }
    )

    with pytest.raises(
        ValueError,
        match="completion_percentage",
    ):
        validate_processed_data(
            df,
            "onboarding_progress",
        )


def test_validate_processed_data_rejects_invalid_assessment_score():
    df = pd.DataFrame(
        {
            "employee_id": [1],
            "learning_record_id": ["L1"],
            "assessment_score": [-5],
        }
    )

    with pytest.raises(
        ValueError,
        match="assessment_score",
    ):
        validate_processed_data(
            df,
            "learning_management",
        )


def test_validate_processed_data_rejects_negative_activity():
    df = pd.DataFrame(
        {
            "employee_id": [1],
            "slack_activity_count": [-1],
        }
    )

    with pytest.raises(
        ValueError,
        match="slack_activity_count",
    ):
        validate_processed_data(
            df,
            "internal_tool_usage",
        )


def test_validate_processed_data_rejects_invalid_employee_dates():
    df = pd.DataFrame(
        {
            "EmpID": [1],
            "DateofHire": pd.to_datetime(
                ["2024-01-10"]
            ),
            "DateofTermination": pd.to_datetime(
                ["2024-01-01"]
            ),
        }
    )

    with pytest.raises(
        ValueError,
        match="DateofTermination cannot be before DateofHire",
    ):
        validate_processed_data(
            df,
            "employee",
        )


def test_validate_processed_data_rejects_invalid_learning_dates():
    df = pd.DataFrame(
        {
            "employee_id": [1],
            "learning_record_id": ["L1"],
            "assigned_date": pd.to_datetime(
                ["2024-01-10"]
            ),
            "completed_date": pd.to_datetime(
                ["2024-01-01"]
            ),
        }
    )

    with pytest.raises(
        ValueError,
        match="completed_date cannot be before assigned_date",
    ):
        validate_processed_data(
            df,
            "learning_management",
        )


def test_preprocess_rejects_unknown_dataset():
    df = pd.DataFrame({"id": [1]})

    with pytest.raises(
        ValueError,
        match="Unknown dataset",
    ):
        preprocess_dataset(
            df,
            "unknown_dataset",
        )


def test_preprocess_rejects_empty_dataset():
    df = pd.DataFrame(
        columns=[
            "EmpID",
            "DateofHire",
            "DateofTermination",
        ]
    )

    with pytest.raises(
        ValueError,
        match="contains no rows",
    ):
        preprocess_dataset(
            df,
            "employee",
        )


def test_onboarding_features():
    df = pd.DataFrame(
        {
            "employee_id": [1, 1, 2],
            "task_status": [
                "Completed",
                "Pending",
                "Completed",
            ],
        }
    )

    result = calculate_onboarding_features(df)

    employee_one = result.loc[
        result["employee_id"] == 1
    ].iloc[0]

    assert employee_one["total_onboarding_tasks"] == 2
    assert employee_one[
        "onboarding_completion_percentage"
    ] == 50


def test_support_ticket_features():
    df = pd.DataFrame(
        {
            "employee_id": [1, 1, 2],
        }
    )

    result = calculate_support_features(df)

    employee_one = result.loc[
        result["employee_id"] == 1
    ].iloc[0]

    assert employee_one["support_ticket_count"] == 2


def test_learning_features():
    df = pd.DataFrame(
        {
            "employee_id": [1, 1, 2],
            "course_status": [
                "Completed",
                "Pending",
                "Completed",
            ],
        }
    )

    result = calculate_learning_features(df)

    employee_one = result.loc[
        result["employee_id"] == 1
    ].iloc[0]

    assert employee_one["learning_completion_rate"] == 50


def test_first_week_activity():
    employee = pd.DataFrame(
        {
            "EmpID": [1],
            "DateofHire": ["2024-01-01"],
        }
    )

    usage = pd.DataFrame(
        {
            "employee_id": [1, 1],
            "usage_date": [
                "2024-01-02",
                "2024-01-10",
            ],
            "slack_activity_count": [5, 10],
            "jira_usage_count": [2, 5],
        }
    )

    result = calculate_first_week_activity(
        usage,
        employee,
    )

    assert result.loc[0, "first_week_activity"] == 7


def test_productivity_indicator():
    df = pd.DataFrame(
        {
            "employee_id": [1],
            "onboarding_completion_percentage": [80],
            "learning_completion_rate": [90],
            "first_week_activity": [10],
        }
    )

    result = calculate_productivity_indicator(df)

    assert result.loc[
        0,
        "productivity_indicator",
    ] == 180