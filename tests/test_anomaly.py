import pandas as pd
import pytest

from src.analysis.anomaly import (
    department_risk_summary,
    detect_anomalies,
    investigate_root_causes,
    run_anomaly_pipeline,
    summarize_anomalies,
)


def create_test_data():
    return pd.DataFrame(
        {
            "employee_id": range(1, 11),
            "onboarding_completion_rate": [
                95, 92, 90, 88, 85, 83, 80, 78, 75, 20
            ],
            "late_onboarding_tasks": [
                0, 1, 1, 2, 2, 3, 3, 4, 5, 20
            ],
            "total_support_tickets": [
                1, 2, 2, 3, 3, 4, 4, 5, 6, 25
            ],
            "open_support_tickets": [
                0, 0, 1, 1, 1, 2, 2, 2, 3, 15
            ],
            "average_resolution_time_hours": [
                2, 3, 4, 5, 5, 6, 7, 8, 9, 50
            ],
            "learning_completion_rate": [
                95, 90, 88, 85, 82, 80, 78, 75, 70, 30
            ],
            "total_tool_usage": [
                20, 19, 18, 17, 16, 15, 14, 13, 12, 5
            ],
            "Department": [
                "IT",
                "IT",
                "HR",
                "HR",
                "Finance",
                "Finance",
                "IT",
                "HR",
                "Finance",
                "IT",
            ],
        }
    )


def test_detect_anomalies_identifies_anomalous_employee():
    df = create_test_data()

    result = detect_anomalies(df)

    assert len(result) == 10
    assert "anomaly_count" in result.columns
    assert "risk_score" in result.columns
    assert "risk_category" in result.columns

    employee = result[result["employee_id"] == 10].iloc[0]

    assert employee["anomaly_count"] > 0
    assert employee["risk_score"] > 0


def test_normal_employees_are_not_flagged_on_every_metric():
    df = create_test_data()

    result = detect_anomalies(df)

    normal_employee = result[result["employee_id"] == 1].iloc[0]

    assert normal_employee["anomaly_count"] == 0
    assert normal_employee["risk_category"] == "Low"


def test_missing_values_are_handled():
    df = create_test_data()

    df.loc[0, "total_support_tickets"] = None
    df.loc[1, "average_resolution_time_hours"] = None

    result = detect_anomalies(df)

    assert len(result) == len(df)
    assert result["employee_id"].notna().all()


def test_invalid_input_without_employee_id():
    df = create_test_data().drop(columns=["employee_id"])

    with pytest.raises(ValueError):
        detect_anomalies(df)


def test_anomaly_summary():
    df = create_test_data()

    anomaly_results = detect_anomalies(df)
    summary = summarize_anomalies(anomaly_results)

    assert not summary.empty
    assert "metric" in summary.columns
    assert "anomaly_count" in summary.columns
    assert "anomaly_percentage" in summary.columns


def test_root_cause_analysis():
    df = create_test_data()

    anomaly_results = detect_anomalies(df)
    root_causes = investigate_root_causes(anomaly_results)

    assert not root_causes.empty
    assert "factor" in root_causes.columns
    assert "high_risk_mean" in root_causes.columns
    assert "other_mean" in root_causes.columns
    assert "difference" in root_causes.columns


def test_department_risk_summary():
    df = create_test_data()

    anomaly_results = detect_anomalies(df)
    summary = department_risk_summary(anomaly_results)

    assert not summary.empty
    assert "Department" in summary.columns
    assert "risk_category" in summary.columns
    assert "employee_count" in summary.columns


def test_empty_input():
    df = pd.DataFrame()

    result = detect_anomalies(df)

    assert result.empty


def test_pipeline_creates_expected_outputs(tmp_path):
    df = create_test_data()

    input_path = tmp_path / "employee_data.csv"
    output_path = tmp_path / "reports"

    df.to_csv(input_path, index=False)

    outputs = run_anomaly_pipeline(
        input_path,
        output_path,
    )

    assert "employee_anomaly_risk" in outputs
    assert "anomaly_summary" in outputs
    assert "root_cause_factors" in outputs
    assert "department_risk_summary" in outputs

    assert (output_path / "employee_anomaly_risk.csv").exists()
    assert (output_path / "anomaly_summary.csv").exists()
    assert (output_path / "root_cause_factors.csv").exists()
    assert (output_path / "department_risk_summary.csv").exists()