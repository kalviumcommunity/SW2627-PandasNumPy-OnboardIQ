"""End-to-end Pandas data pipeline for OnboardIQ."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ingestion.loader import load_csv
from src.preprocessing.cleaning import preprocess_dataset
from src.transformation.merge import merge_employee_data
from src.utils.logging_utils import setup_logger


logger = setup_logger("onboardiq.pipeline")


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

DATASET_CONFIG = {
    "employee": {
        "file": "employee.csv",
        "primary_key": "EmpID",
    },
    "onboarding_progress": {
        "file": "onboarding_progress.csv",
        "primary_key": "onboarding_task_id",
    },
    "internal_tool_usage": {
        "file": "internal_tool_usage.csv",
        "primary_key": "usage_id",
    },
    "support_tickets": {
        "file": "support_tickets.csv",
        "primary_key": "ticket_id",
    },
    "learning_management": {
        "file": "learning_management.csv",
        "primary_key": "learning_record_id",
    },
}


def load_and_preprocess_dataset(
    dataset_name: str,
) -> pd.DataFrame:
    """Load and preprocess one configured raw dataset."""

    if dataset_name not in DATASET_CONFIG:
        raise ValueError(
            f"Unknown dataset: {dataset_name}"
        )

    configuration = DATASET_CONFIG[dataset_name]

    input_path = RAW_DATA_DIR / configuration["file"]

    dataframe = load_csv(
        input_path,
        primary_key=configuration["primary_key"],
    )

    processed = preprocess_dataset(
        dataframe,
        dataset_name,
    )

    logger.info(
        "Processed %s dataset: %s rows, %s columns.",
        dataset_name,
        len(processed),
        len(processed.columns),
    )

    return processed


def run_data_pipeline(
    output_path: str | Path | None = None,
) -> pd.DataFrame:
    """
    Run the complete OnboardIQ data pipeline.

    Workflow:

        Raw CSV
            ↓
        Ingestion validation
            ↓
        Preprocessing
            ↓
        Employee-level aggregation
            ↓
        Final analytical dataset

    Returns:
        Employee-level merged analytical DataFrame.
    """

    logger.info("Starting OnboardIQ data pipeline.")

    datasets = {
        dataset_name: load_and_preprocess_dataset(dataset_name)
        for dataset_name in DATASET_CONFIG
    }

    result = merge_employee_data(
        employee=datasets["employee"],
        onboarding=datasets["onboarding_progress"],
        tool_usage=datasets["internal_tool_usage"],
        support_tickets=datasets["support_tickets"],
        learning=datasets["learning_management"],
    )

    if output_path is None:
        output_path = (
            PROCESSED_DATA_DIR
            / "employee_onboarding_analytics.csv"
        )
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        output_path,
        index=False,
    )

    logger.info(
        "Data pipeline completed successfully. "
        "Output: %s | Shape: %s",
        output_path,
        result.shape,
    )

    return result


if __name__ == "__main__":
    run_data_pipeline()