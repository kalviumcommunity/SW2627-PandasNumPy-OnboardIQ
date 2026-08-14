from pathlib import Path

import pandas as pd


DATASET_SCHEMAS = {
    "employee": {
        "integer": [
            "EmpID",
            "MarriedID",
            "MaritalStatusID",
            "GenderID",
            "EmpStatusID",
            "DeptID",
            "PerfScoreID",
            "PositionID",
            "Termd",
            "Absences",
            "DaysLateLast30",
            "SpecialProjectsCount",
        ],
        "numeric": ["Salary"],
        "datetime": [
            "DOB",
            "DateofHire",
            "DateofTermination",
            "LastPerformanceReview_Date",
        ],
        "text": [],
    },
    "onboarding_progress": {
        "integer": ["employee_id"],
        "numeric": ["completion_percentage"],
        "datetime": ["due_date", "completed_date"],
        "text": [
            "onboarding_task_id",
            "task_name",
            "task_category",
            "current_stage",
            "task_status",
        ],
    },
    "internal_tool_usage": {
        "integer": [
            "employee_id",
            "slack_activity_count",
            "jira_usage_count",
            "github_activity_count",
            "teams_activity_count",
            "workspace_activity_count",
        ],
        "numeric": [],
        "datetime": ["usage_date"],
        "text": [],
    },
    "support_tickets": {
        "integer": ["employee_id"],
        "numeric": ["resolution_time_hours"],
        "datetime": ["created_date"],
        "text": [
            "ticket_id",
            "issue_category",
            "priority",
            "assigned_team",
            "status",
        ],
    },
    "learning_management": {
        "integer": ["employee_id"],
        "numeric": ["assessment_score", "completion_time_hours"],
        "datetime": ["assigned_date", "completed_date"],
        "text": [
            "learning_record_id",
            "course_name",
            "course_type",
            "course_status",
        ],
    },
}


MISSING_RULES = {
    "DateofTermination": "Preserve null: employee may still be active.",
    "ManagerID": "Preserve null: manager information may be unavailable.",
    "completed_date": "Preserve null when task/course is incomplete.",
    "resolution_time_hours": "Preserve null when ticket is unresolved.",
    "assessment_score": "Preserve null when assessment is not applicable/not completed.",
    "completion_time_hours": "Preserve null when course is incomplete.",
}


def standardize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize text and categorical columns.

    Rules:
    - Convert text-like columns to Pandas string dtype.
    - Remove leading and trailing whitespace.
    - Collapse repeated internal whitespace.
    """
    result = df.copy()

    for column in result.select_dtypes(
        include=["object", "string", "category"]
    ).columns:
        result[column] = (
            result[column]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

    return result


def remove_duplicate_rows(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove exact duplicate records while preserving the first occurrence.
    """
    result = df.copy()

    return result.drop_duplicates().reset_index(drop=True)


def convert_data_types(
    df: pd.DataFrame,
    schema: dict,
) -> pd.DataFrame:
    """Convert available columns to the required Pandas data types."""
    result = df.copy()

    for column in schema.get("integer", []):
        if column in result.columns:
            result[column] = pd.to_numeric(
                result[column], errors="coerce"
            ).astype("Int64")

    for column in schema.get("numeric", []):
        if column in result.columns:
            result[column] = pd.to_numeric(
                result[column], errors="coerce"
            )

    for column in schema.get("datetime", []):
        if column in result.columns:
            result[column] = pd.to_datetime(
                result[column], errors="coerce"
            )

    for column in schema.get("text", []):
        if column in result.columns:
            result[column] = result[column].astype("string").str.strip()

    return result


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preserve business-meaningful null values.

    No arbitrary zero, date, or 'Unknown' values are introduced.
    """
    return df.copy()


def add_date_features(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """Create meaningful date-derived features."""
    result = df.copy()

    if dataset_name == "employee" and "DateofHire" in result.columns:
        end_date = result.get("DateofTermination", pd.Series(pd.NaT, index=result.index))
        end_date = end_date.fillna(pd.Timestamp.today().normalize())
        result["tenure_days"] = (end_date - result["DateofHire"]).dt.days

    elif dataset_name == "onboarding_progress" and {"due_date", "completed_date"}.issubset(result.columns):
        result["days_overdue"] = (result["completed_date"] - result["due_date"]).dt.days.clip(lower=0)

    elif dataset_name == "learning_management" and {"assigned_date", "completed_date"}.issubset(result.columns):
        result["learning_duration_days"] = (result["completed_date"] - result["assigned_date"]).dt.days

    return result


def detect_iqr_outliers(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Flag IQR-based statistical outliers without removing rows."""
    result = df.copy()
    for column in columns:
        if column not in result.columns:
            continue
        values = result[column].dropna()
        if values.empty:
            continue
        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        result[f'{column}_outlier'] = result[column].notna() & ((result[column] < lower) | (result[column] > upper))
    return result


def validate_processed_data(
    df: pd.DataFrame,
    dataset_name: str,
) -> None:
    """Run basic post-processing validation checks."""

    if df.empty:
        raise ValueError(f"{dataset_name} contains no rows.")

    schema = DATASET_SCHEMAS[dataset_name]

    primary_keys = {
        "employee": "EmpID",
        "onboarding_progress": "onboarding_task_id",
        "internal_tool_usage": "usage_id",
        "support_tickets": "ticket_id",
        "learning_management": "learning_record_id",
    }

    primary_key = primary_keys.get(dataset_name)

    if primary_key in df.columns:
        if df[primary_key].isna().any():
            raise ValueError(
                f"{dataset_name}: primary key '{primary_key}' contains nulls."
            )

        if df[primary_key].duplicated().any():
            raise ValueError(
                f"{dataset_name}: duplicate primary keys found."
            )

    if "completion_percentage" in df.columns:
        if (
            df["completion_percentage"].dropna().lt(0).any()
            or df["completion_percentage"].dropna().gt(100).any()
        ):
            raise ValueError(
                "completion_percentage must be between 0 and 100."
            )

    if "assessment_score" in df.columns:
        if (
            df["assessment_score"].dropna().lt(0).any()
            or df["assessment_score"].dropna().gt(100).any()
        ):
            raise ValueError(
                "assessment_score must be between 0 and 100."
            )

    for column in [
        "slack_activity_count",
        "jira_usage_count",
        "github_activity_count",
        "teams_activity_count",
        "workspace_activity_count",
        "resolution_time_hours",
        "completion_time_hours",
    ]:
        if column in df.columns and df[column].dropna().lt(0).any():
            raise ValueError(f"{column} cannot contain negative values.")

    if "DateofHire" in df.columns and "DateofTermination" in df.columns:
        valid_dates = (
            df["DateofTermination"].notna()
            & df["DateofHire"].notna()
        )

        if (
            df.loc[valid_dates, "DateofTermination"]
            < df.loc[valid_dates, "DateofHire"]
        ).any():
            raise ValueError(
                "DateofTermination cannot be before DateofHire."
            )

    if "assigned_date" in df.columns and "completed_date" in df.columns:
        valid_dates = (
            df["assigned_date"].notna()
            & df["completed_date"].notna()
        )

        if (
            df.loc[valid_dates, "completed_date"]
            < df.loc[valid_dates, "assigned_date"]
        ).any():
            raise ValueError(
                "Learning completed_date cannot be before assigned_date."
            )

    for column in schema.get("datetime", []):
        if column in df.columns and not (
            pd.api.types.is_datetime64_any_dtype(df[column])
        ):
            raise TypeError(
                f"{dataset_name}: {column} is not a datetime column."
            )


def preprocess_dataset(
    df: pd.DataFrame,
    dataset_name: str,
) -> pd.DataFrame:
    """Run the complete preprocessing workflow for one dataset."""
    if dataset_name not in DATASET_SCHEMAS:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    result = standardize_text_columns(df)
    result = remove_duplicate_rows(result)
    result = convert_data_types(
        result,
        DATASET_SCHEMAS[dataset_name],
    )
    result = handle_missing_values(result)
    result = add_date_features(result, dataset_name)

    outlier_columns = [
        "Salary", "Absences", "DaysLateLast30",
        "SpecialProjectsCount", "resolution_time_hours",
        "assessment_score", "completion_time_hours",
    ]
    result = detect_iqr_outliers(result, outlier_columns)

    validate_processed_data(result, dataset_name)

    return result


def process_csv(
    input_path: str | Path,
    output_path: str | Path,
    dataset_name: str,
) -> pd.DataFrame:
    """Load, preprocess, validate, and save one CSV dataset."""

    input_path = Path(input_path)
    output_path = Path(output_path)

    df = pd.read_csv(input_path)

    processed = preprocess_dataset(df, dataset_name)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(output_path, index=False)

    return processed

def test_date_features_are_created():
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


def test_iqr_outlier_is_flagged_without_removing_rows():
    df = pd.DataFrame(
        {
            "EmpID": [1, 2, 3, 4, 5],
            "Salary": [50000, 51000, 52000, 53000, 200000],
            "DateofHire": [
                "2024-01-01",
                "2024-01-01",
                "2024-01-01",
                "2024-01-01",
                "2024-01-01",
            ],
            "DateofTermination": [None, None, None, None, None],
        }
    )

    result = preprocess_dataset(df, "employee")

    assert len(result) == 5
    assert result.loc[4, "Salary_outlier"] is True
    assert result.loc[0, "Salary_outlier"] is False
