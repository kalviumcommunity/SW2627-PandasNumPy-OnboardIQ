import pandas as pd
from typing import Dict, Any

def calculate_dashboard_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Minimal, defensive KPI calculator used by the dashboard.
    Expects optional columns:
      - onboarding_completed (bool/0-1)
      - learning_completed (bool/0-1)
      - tool_adopted (bool/0-1)
      - support_tickets (numeric)
      - assessment_score (numeric)
    Returns a dict with keys the dashboard expects.
    """
    if df is None or df.empty:
        return {}

    def pct(col: str) -> float:
        if col in df.columns:
            try:
                return float(df[col].dropna().astype(float).mean() * 100)
            except Exception:
                return 0.0
        return 0.0

    def mean(col: str) -> float:
        if col in df.columns:
            try:
                return float(df[col].dropna().astype(float).mean())
            except Exception:
                return 0.0
        return 0.0

    employee_count = int(len(df))

    onboarding_completion_rate = pct("onboarding_completed")
    learning_completion_rate = pct("learning_completed")
    tool_adoption_rate = pct("tool_adopted")
    average_support_tickets = mean("support_tickets")
    average_assessment_score = mean("assessment_score")

    # Simple composite for productivity readiness (fallback if no explicit column)
    productivity_readiness_score = (
        (
            onboarding_completion_rate
            + learning_completion_rate
            + tool_adoption_rate
        ) / 3.0
    )

    return {
        "employee_count": employee_count,
        "onboarding_completion_rate": onboarding_completion_rate,
        "learning_completion_rate": learning_completion_rate,
        "tool_adoption_rate": tool_adoption_rate,
        "average_support_tickets": average_support_tickets,
        "average_assessment_score": average_assessment_score,
        "productivity_readiness_score": productivity_readiness_score,
    }