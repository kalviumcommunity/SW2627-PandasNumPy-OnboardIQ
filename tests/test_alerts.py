import pandas as pd
import pytest

from src.analysis.alerts import (
    DEFAULT_THRESHOLDS,
    detect_kpi_alerts,
    get_active_alerts,
    summarize_alerts,
)


def test_default_thresholds_exist():
    assert "onboarding_completion_rate" in DEFAULT_THRESHOLDS
    assert "learning_completion_rate" in DEFAULT_THRESHOLDS
    assert "tool_adoption_rate" in DEFAULT_THRESHOLDS
    assert "productivity_readiness_score" in DEFAULT_THRESHOLDS


def test_kpis_within_thresholds_are_normal():
    kpis = {
        "onboarding_completion_rate": 90,
        "learning_completion_rate": 85,
        "tool_adoption_rate": 88,
        "productivity_readiness_score": 80,
    }

    result = detect_kpi_alerts(kpis)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 4
    assert (result["severity"] == "Normal").all()


def test_warning_threshold_is_detected():
    kpis = {
        "onboarding_completion_rate": 70,
    }

    result = detect_kpi_alerts(kpis)

    row = result.iloc[0]

    assert row["severity"] == "Warning"
    assert row["status"] == "Warning"


def test_critical_threshold_is_detected():
    kpis = {
        "onboarding_completion_rate": 40,
    }

    result = detect_kpi_alerts(kpis)

    row = result.iloc[0]

    assert row["severity"] == "Critical"
    assert row["status"] == "Critical"


def test_active_alerts_exclude_normal_kpis():
    kpis = {
        "onboarding_completion_rate": 90,
        "learning_completion_rate": 60,
    }

    alerts = detect_kpi_alerts(kpis)
    active = get_active_alerts(alerts)

    assert len(active) == 1
    assert active.iloc[0]["severity"] == "Warning"


def test_alert_summary():
    kpis = {
        "onboarding_completion_rate": 40,
        "learning_completion_rate": 60,
        "tool_adoption_rate": 90,
    }

    alerts = detect_kpi_alerts(kpis)
    summary = summarize_alerts(alerts)

    assert summary["total_alerts"] == 2
    assert summary["critical_alerts"] == 1
    assert summary["warning_alerts"] == 1


def test_missing_kpi_is_ignored():
    kpis = {
        "onboarding_completion_rate": 90,
    }

    result = detect_kpi_alerts(kpis)

    assert len(result) == 1
    assert result.iloc[0]["severity"] == "Normal"


def test_invalid_kpi_input():
    with pytest.raises(ValueError):
        detect_kpi_alerts(None)