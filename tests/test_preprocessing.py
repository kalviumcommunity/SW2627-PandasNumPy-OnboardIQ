import pandas as pd

from src.preprocessing.cleaning import (
    preprocess_dataset,
    remove_duplicate_rows,
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