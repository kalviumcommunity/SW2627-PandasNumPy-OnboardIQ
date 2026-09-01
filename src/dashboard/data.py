import pandas as pd
from pathlib import Path
from typing import Optional

def load_dashboard_dataset() -> Optional[pd.DataFrame]:
    """
    Load a dashboard dataset if present at data/employee_data.csv (project root).
    Returns an empty DataFrame if no file is found.
    """
    repo_root = Path(__file__).resolve().parents[2]
    csv_path = repo_root / "data" / "employee_data.csv"

    if csv_path.exists():
        try:
            return pd.read_csv(csv_path)
        except Exception:
            # If the CSV cannot be read, return empty dataframe so callers handle it
            return pd.DataFrame()
    return pd.DataFrame()