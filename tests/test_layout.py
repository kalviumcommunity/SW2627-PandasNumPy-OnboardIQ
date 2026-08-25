import pytest
from unittest.mock import patch, MagicMock
from src.dashboard.layout import render_kpi_cards, render_insight_narratives


@patch("src.dashboard.layout.st")
def test_render_kpi_cards(mock_st):
    """Test that KPI cards render the correct number of metrics."""
    # Mock the 4 columns returned by st.columns(4)
    mock_st.columns.return_value = [MagicMock() for _ in range(4)]
    
    kpis = {
        "employee_count": 100,
        "onboarding_completion_rate": 85.0,
        "learning_completion_rate": 75.0,
        "tool_adoption_rate": 90.0,
        "average_support_tickets": 2.5,
        "average_assessment_score": 80.0,
        "productivity_readiness_score": 85.0,
    }
    health = {
        "onboarding_health": "healthy",
        "learning_health": "attention",
        "tool_adoption_health": "healthy",
        "support_health": "critical",
    }
    
    render_kpi_cards(kpis, health=health)
    
    # Verify we created exactly 7 metric cards
    assert mock_st.metric.call_count == 7


@patch("src.dashboard.layout.st")
def test_render_insight_narratives(mock_st):
    """Test that insight narratives render the subheader and bullet points."""
    kpis = {
        "onboarding_completion_rate": 85.0,
        "learning_completion_rate": 75.0,
        "tool_adoption_rate": 90.0,
        "open_ticket_rate": 10.0,
    }
    health = {
        "onboarding_health": "healthy",
        "learning_health": "attention",
        "tool_adoption_health": "healthy",
        "support_health": "healthy",
    }
    
    render_insight_narratives(kpis, health=health)
    
    # Verify the subheader was called
    mock_st.subheader.assert_called_once()
    # Verify we generated exactly 4 insight bullet points
    assert mock_st.markdown.call_count == 4