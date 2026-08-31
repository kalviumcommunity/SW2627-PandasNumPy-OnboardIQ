import pandas as pd
import pytest

from src.utils.export_utils import export_dataframe_to_csv, generate_executive_report


def test_export_dataframe_to_csv_normal():
    """Test exporting a valid, non-empty DataFrame."""
    df = pd.DataFrame({
        "employee_id": [10026, 10084],
        "Department": ["Production", "IT/IS"],
        "onboarding_completion_rate": [71.4, 78.5]
    })
    
    csv_bytes = export_dataframe_to_csv(df)
    
    assert isinstance(csv_bytes, bytes)
    assert b"employee_id,Department,onboarding_completion_rate" in csv_bytes
    assert b"10026,Production,71.4" in csv_bytes


def test_export_dataframe_to_csv_empty():
    """Test that exporting an empty DataFrame raises a ValueError."""
    df = pd.DataFrame()
    
    with pytest.raises(ValueError, match="Cannot export an empty dataframe."):
        export_dataframe_to_csv(df)


def test_generate_executive_report_healthy():
    """Test report generation when all KPIs are healthy."""
    kpis = {
        "employee_count": 150,
        "onboarding_completion_rate": 85.0,
        "learning_completion_rate": 82.0,
        "tool_adoption_rate": 90.0,
        "average_support_tickets": 1.5,
        "productivity_readiness_score": 85.5
    }
    health = {
        "onboarding_health": "healthy",
        "learning_health": "healthy",
        "tool_adoption_health": "healthy",
        "support_health": "healthy"
    }
    
    report = generate_executive_report(kpis, health)
    
    assert "# OnboardIQ Executive Summary Report" in report
    assert "**Total Employees:** 150" in report
    assert "Maintain current onboarding protocols" in report
    assert "Action Required" not in report


def test_generate_executive_report_attention():
    """Test report generation when some KPIs need attention."""
    kpis = {
        "employee_count": 50,
        "onboarding_completion_rate": 55.0,
        "learning_completion_rate": 65.0,
        "tool_adoption_rate": 45.0,
        "average_support_tickets": 5.0,
        "productivity_readiness_score": 55.0
    }
    health = {
        "onboarding_health": "critical",
        "learning_health": "attention",
        "tool_adoption_health": "critical",
        "support_health": "attention"
    }
    
    report = generate_executive_report(kpis, health)
    
    assert "Action Required" in report
    assert "Review onboarding workflows" in report
    assert "barriers to internal tool adoption" in report