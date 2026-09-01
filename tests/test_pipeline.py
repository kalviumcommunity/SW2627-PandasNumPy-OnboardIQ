import pandas as pd
import pytest

from src.pipeline import (
    load_and_preprocess_dataset,
    run_data_pipeline,
)


def test_load_and_preprocess_employee_dataset():
    result = load_and_preprocess_dataset("employee")

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "EmpID" in result.columns


def test_load_and_preprocess_onboarding_dataset():
    result = load_and_preprocess_dataset(
        "onboarding_progress"
    )

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "employee_id" in result.columns


def test_unknown_dataset_raises_error():
    with pytest.raises(ValueError, match="Unknown dataset"):
        load_and_preprocess_dataset("invalid_dataset")


def test_run_data_pipeline_returns_employee_level_dataset(
    tmp_path,
):
    output_path = (
        tmp_path / "employee_onboarding_analytics.csv"
    )

    result = run_data_pipeline(output_path)

    assert isinstance(result, pd.DataFrame)
    assert not result.empty

    assert "EmpID" in result.columns
    assert "employee_id" in result.columns

    assert len(result) == 311
    assert result["EmpID"].nunique() == 311
    assert not result["EmpID"].duplicated().any()

    assert output_path.exists()


def test_pipeline_output_can_be_reloaded(tmp_path):
    output_path = (
        tmp_path / "employee_onboarding_analytics.csv"
    )

    run_data_pipeline(output_path)

    reloaded = pd.read_csv(output_path)

    assert len(reloaded) == 311
    assert "EmpID" in reloaded.columns
    assert "onboarding_completion_rate" in reloaded.columns
    assert "learning_completion_rate" in reloaded.columns
    assert "total_support_tickets" in reloaded.columns