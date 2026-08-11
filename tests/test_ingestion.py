import json

import pandas as pd
import pytest

from src.ingestion.loader import load_csv, load_json


def test_load_valid_csv(tmp_path):
    csv_file = tmp_path / "employees.csv"

    pd.DataFrame(
        {
            "EmpID": [1, 2],
            "Name": ["Alice", "Bob"],
        }
    ).to_csv(csv_file, index=False)

    dataframe = load_csv(csv_file)

    assert isinstance(dataframe, pd.DataFrame)
    assert dataframe.shape == (2, 2)
    assert list(dataframe.columns) == ["EmpID", "Name"]


def test_load_valid_json(tmp_path):
    json_file = tmp_path / "employees.json"

    data = [
        {"EmpID": 1, "Name": "Alice"},
        {"EmpID": 2, "Name": "Bob"},
    ]

    json_file.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    dataframe = load_json(json_file)

    assert isinstance(dataframe, pd.DataFrame)
    assert dataframe.shape == (2, 2)
    assert list(dataframe.columns) == ["EmpID", "Name"]


def test_missing_file_raises_error(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_csv(missing_file)


def test_unsupported_extension_raises_error(tmp_path):
    text_file = tmp_path / "employees.txt"

    text_file.write_text(
        "EmpID,Name\n1,Alice\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Unsupported file extension",
    ):
        load_csv(text_file)


def test_empty_csv_raises_error(tmp_path):
    csv_file = tmp_path / "empty.csv"

    csv_file.write_text(
        "",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_csv(csv_file)


def test_empty_json_raises_error(tmp_path):
    json_file = tmp_path / "empty.json"

    json_file.write_text(
        "[]",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="unexpectedly empty",
    ):
        load_json(json_file)


def test_malformed_json_raises_error(tmp_path):
    json_file = tmp_path / "malformed.json"

    json_file.write_text(
        '{"EmpID": 1, "Name": ',
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Malformed or invalid JSON",
    ):
        load_json(json_file)


def test_required_columns_are_validated(tmp_path):
    csv_file = tmp_path / "employees.csv"

    pd.DataFrame(
        {
            "EmpID": [1, 2],
            "Name": ["Alice", "Bob"],
        }
    ).to_csv(csv_file, index=False)

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        load_csv(
            csv_file,
            required_columns=["EmpID", "Department"],
        )


def test_duplicate_primary_keys_are_reported(tmp_path, caplog):
    csv_file = tmp_path / "employees.csv"

    pd.DataFrame(
        {
            "EmpID": [1, 1, 2],
            "Name": ["Alice", "Alice", "Bob"],
        }
    ).to_csv(csv_file, index=False)

    with caplog.at_level("WARNING"):
        dataframe = load_csv(
            csv_file,
            primary_key="EmpID",
        )

    assert len(dataframe) == 3
    assert "duplicate values in primary key" in caplog.text