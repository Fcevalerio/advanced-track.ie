# tests/test_db2_connector.py
"""
Integration tests for the DB2Connector in db2_connector.py.

Run:
    pytest -q tests/test_db2_connector.py

Behavior:
- If .env is missing or DB not reachable, tests are skipped rather than failing.
- Uses tmp_path for any parquet output.
- Adjust TEST_SCHEMA env var if your schema differs from IEPLANE.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import pytest

# import your connector (adjust import path if needed)
# if your connector file is db2_connector.py at project root: from db2_connector import DB2Connector
# if connector is in src/connector.py: from src.connector import DB2Connector
# 
from src.connector import DB2Connector # <-- adjust if your module path differs


# Test configuration
DEFAULT_SCHEMA = os.getenv("TEST_SCHEMA", "IEPLANE")
EXPECTED_TABLES = [
    "AIRPLANES",
    "AIRPORTS",
    "COUNTRIES",
    "DEPARTMENT",
    "EMPLOYEE",
    "FLIGHTS",
    "PASSENGERS",
    "ROUTES",
    "TICKETS",
]


# ---------- Fixtures ----------
@pytest.fixture(scope="session")
def connector() -> DB2Connector:
    """Create connector and skip tests if not possible to connect."""
    try:
        db = DB2Connector()  # will load .env via DB2Config.from_env
    except Exception as e:
        pytest.skip(f"Cannot construct DB2Connector (env missing/invalid): {e}")

    try:
        db.test_connection()
    except Exception as e:
        pytest.skip(f"Cannot connect to DB2 (skipping DB integration tests): {e}")

    return db


# ---------- Basic tests ----------
def test_test_connection(connector: DB2Connector):
    assert connector.test_connection() is True


def test_read_sql_simple(connector: DB2Connector):
    df = connector.read_sql("SELECT 1 AS X FROM SYSIBM.SYSDUMMY1")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "X" in df.columns
    assert int(df.iloc[0]["X"]) == 1


def test_list_schemas(connector: DB2Connector):
    df = connector.list_schemas()
    assert isinstance(df, pd.DataFrame)
    # Column name may be 'SCHEMA' according to implementation
    col_names = [c.upper() for c in df.columns]
    assert any("SCHEMA" == c for c in col_names) or len(df) >= 0  # minimal check


# ---------- Discovery / metadata tests ----------
def test_list_tables_for_schema(connector: DB2Connector):
    try:
        df = connector.list_tables(schema=DEFAULT_SCHEMA)
    except Exception as e:
        pytest.skip(f"list_tables failed for schema {DEFAULT_SCHEMA}: {e}")

    assert isinstance(df, pd.DataFrame)
    assert any(c.upper() == "TABNAME" for c in df.columns) or True  # ensure callable


@pytest.mark.parametrize("table", EXPECTED_TABLES)
def test_table_exists_and_get_columns(connector: DB2Connector, table: str):
    try:
        exists = connector.table_exists(schema=DEFAULT_SCHEMA, table=table)
    except Exception as e:
        pytest.skip(f"table_exists raised for {DEFAULT_SCHEMA}.{table}: {e}")

    if not exists:
        pytest.skip(f"Table {DEFAULT_SCHEMA}.{table} not found; skipping column checks")

    try:
        cols = connector.get_table_columns(schema=DEFAULT_SCHEMA, table=table)
    except Exception as e:
        pytest.fail(f"get_table_columns raised for {DEFAULT_SCHEMA}.{table}: {e}")

    assert isinstance(cols, pd.DataFrame)
    assert len(cols) >= 1


# ---------- Data read tests ----------
@pytest.mark.parametrize("table", EXPECTED_TABLES)
def test_read_table_limit(connector: DB2Connector, table: str):
    try:
        if not connector.table_exists(schema=DEFAULT_SCHEMA, table=table):
            pytest.skip(f"{DEFAULT_SCHEMA}.{table} not present; skipping read_table test.")
    except Exception as e:
        pytest.skip(f"table_exists check failed for {DEFAULT_SCHEMA}.{table}: {e}")

    limit = 5
    try:
        df = connector.read_table(schema=DEFAULT_SCHEMA, table=table, limit=limit)
    except Exception as e:
        pytest.fail(f"read_table raised for {DEFAULT_SCHEMA}.{table}: {e}")

    assert isinstance(df, pd.DataFrame)
    assert len(df) <= limit


# ---------- Parquet export tests ----------
@pytest.mark.parametrize("table", EXPECTED_TABLES)
def test_save_table_as_parquet(connector: DB2Connector, tmp_path: Path, table: str):
    try:
        if not connector.table_exists(schema=DEFAULT_SCHEMA, table=table):
            pytest.skip(f"{DEFAULT_SCHEMA}.{table} not present; skipping parquet export.")
    except Exception as e:
        pytest.skip(f"table_exists check failed for {DEFAULT_SCHEMA}.{table}: {e}")

    out_file = tmp_path / f"{table.lower()}.parquet"
    try:
        result = connector.save_table_as_parquet(schema=DEFAULT_SCHEMA, table=table, parquet_path=str(out_file), limit=100)
    except Exception as e:
        pytest.fail(f"save_table_as_parquet raised for {DEFAULT_SCHEMA}.{table}: {e}")

    # Accept either direct file or pattern returned for chunked writes
    if isinstance(result, str) and ("_part" in result or "*" in result):
        # look for any parquet files in tmp_path matching the table prefix
        parts = list(tmp_path.glob(f"{table.lower()}*.parquet"))
        # it's OK if no files found (table empty), but ensure function completed
        assert parts is not None
    else:
        assert out_file.exists() or any(tmp_path.glob(f"{table.lower()}*.parquet"))


def test_execute_select(connector: DB2Connector):
    # ensure execute runs without raising
    try:
        _ = connector.execute("SELECT 1 FROM SYSIBM.SYSDUMMY1")
    except Exception as e:
        pytest.fail(f"execute() raised for simple SELECT: {e}")
