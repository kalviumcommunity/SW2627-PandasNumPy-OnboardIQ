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
