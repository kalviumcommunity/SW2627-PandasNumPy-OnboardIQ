from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Project information
PROJECT_NAME = "OnboardIQ"
APP_NAME = "Employee Onboarding Analytics Dashboard"
VERSION = "0.1.0"


# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ERROR_DATA_DIR = DATA_DIR / "errors"
SAMPLE_DATA_DIR = DATA_DIR / "sample"


# Logs
LOG_DIR = BASE_DIR / "logs"


# Database
DATABASE_NAME = "employee_onboarding.db"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / DATABASE_NAME