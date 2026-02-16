# db2_connector.py
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional, Union

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


# -------------------------
# Config
# -------------------------
@dataclass(frozen=True)
class DB2Config:
    host: str
    port: int
    database: str
    username: str
    password: str
    driver: str = "db2+ibm_db"

    @staticmethod
    def from_env(env_path: Optional[str] = None) -> "DB2Config":
        """
        Loads DB2 credentials from environment variables (optionally via .env file).
        Required:
          DB2_HOST, DB2_PORT, DB2_DATABASE, DB2_USERNAME, DB2_PASSWORD
        Optional:
          DB2_DRIVER (defaults to db2+ibm_db)
        """
        if env_path:
            load_dotenv(env_path)
        else:
            load_dotenv()  # loads .env if present

        def must_get(name: str) -> str:
            val = os.getenv(name)
            if not val:
                raise ValueError(f"Missing required env var: {name}")
            return val

        return DB2Config(
            host=must_get("DB_HOST"),
            port=int(must_get("DB_PORT")),
            database=must_get("DB_NAME"),
            username=must_get("DB_USERNAME"),
            password=must_get("DB_PASSWORD"),
            driver=os.getenv("DB2_DRIVER", "db2+ibm_db"),
        )

    def connection_string(self) -> str:
        # db2+ibm_db://<username>:<password>@<host>:<port>/<database>
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


# -------------------------
# Connector
# -------------------------
class DB2Connector:
    """
    DB2 connector for:
      - creating a SQLAlchemy Engine
      - running queries into pandas DataFrames
      - listing schemas/tables
      - reading tables (schema required)
      - exporting query/table results to Parquet
    """

    def __init__(
        self,
        config: Optional[DB2Config] = None,
        env_path: Optional[str] = None,
        *,
        echo: bool = False,
    ):
        self.config = config or DB2Config.from_env(env_path=env_path)
        self._engine: Engine = create_engine(self.config.connection_string(), echo=echo)

    @property
    def engine(self) -> Engine:
        return self._engine

    # -------------------------
    # Core ops
    # -------------------------
    def test_connection(self) -> bool:
        """
        Lightweight connectivity check.
        """
        with self.engine.connect() as conn:
            conn.execute(text("SELECT 1 FROM SYSIBM.SYSDUMMY1"))
        return True

    def read_sql(
        self,
        query: str,
        params: Optional[Union[Dict[str, Any], tuple, list]] = None,
        *,
        chunksize: Optional[int] = None,
    ):
        if chunksize:
            return pd.read_sql(query, self.engine, params=params, chunksize=chunksize)
        return pd.read_sql(query, self.engine, params=params)


    def execute(self, statement: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        Execute a SQL statement (INSERT/UPDATE/DELETE/DDL).
        Returns affected rowcount when available.
        """
        with self.engine.begin() as conn:
            result = conn.execute(text(statement), params or {})
            return int(getattr(result, "rowcount", 0) or 0)

    # -------------------------
    # Discovery helpers
    # -------------------------
    def list_schemas(self) -> pd.DataFrame:
        """
        List available schemas.
        """
        q = """
        SELECT DISTINCT TRIM(SCHEMANAME) AS SCHEMA
        FROM SYSCAT.SCHEMATA
        ORDER BY SCHEMA
        """
        return self.read_sql(q)

    def list_tables(self, schema: str, table_type: str = "T") -> pd.DataFrame:
        """
        List tables/views in a schema.
        table_type:
          'T' = base tables
          'V' = views
          'A' = aliases
          etc.
        """
        q = """
        SELECT
            TRIM(TABSCHEMA) AS TABSCHEMA,
            TRIM(TABNAME)   AS TABNAME,
            TYPE            AS TYPE
        FROM SYSCAT.TABLES
        WHERE TABSCHEMA = ?
        AND TYPE = ?
        ORDER BY TABNAME
        """
        return self.read_sql(q, params=(schema.upper(), table_type))

    def list_views(self, schema: str) -> pd.DataFrame:
        """
        Convenience: list views in a schema.
        """
        return self.list_tables(schema=schema, table_type="V")

    def table_exists(self, schema: str, table: str) -> bool:
        """
        Check if schema.table exists.
        """
        q = """
        SELECT 1
        FROM SYSCAT.TABLES
        WHERE TABSCHEMA = ? AND TABNAME = ?
        FETCH FIRST 1 ROWS ONLY
        """
        df = self.read_sql(q, params=(schema.upper(), table.upper()))
        return not df.empty

    def get_table_columns(self, schema: str, table: str) -> pd.DataFrame:
        """
        Return column metadata for schema.table.
        """
        q = """
        SELECT
            COLNO,
            TRIM(COLNAME) AS COLNAME,
            TYPENAME,
            LENGTH,
            SCALE,
            NULLS
        FROM SYSCAT.COLUMNS
        WHERE TABSCHEMA = ?
        AND TABNAME   = ?
        ORDER BY COLNO
        """
        return self.read_sql(q, params=(schema.upper(), table.upper()))
    
    # -------------------------
    # Table read helpers (schema required)
    # -------------------------
    def read_table(
        self,
        schema: str,
        table: str,
        *,
        limit: Optional[int] = None,
        columns: Optional[list[str]] = None,
        where: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Read a table (optionally limited / filtered).
        NOTE: schema is required (no defaults).
        """
        col_sql = ", ".join(columns) if columns else "*"
        sql = f"SELECT {col_sql} FROM {schema}.{table}"
        if where:
            sql += f" WHERE {where}"
        if limit is not None:
            sql += f" FETCH FIRST {int(limit)} ROWS ONLY"
        return self.read_sql(sql)

    def sample_table(self, schema: str, table: str, n: int = 10) -> pd.DataFrame:
        """
        Quick peek at first n rows from schema.table.
        """
        return self.read_table(schema=schema, table=table, limit=n)

    # -------------------------
    # Export helpers
    # -------------------------
    def save_query_as_parquet(
        self,
        query: str,
        parquet_path: str,
        params: Optional[Dict[str, Any]] = None,
        *,
        chunksize: Optional[int] = None,
    ) -> str:
        """
        Save query results to a Parquet file.

        If chunksize is provided, this implementation writes each chunk to a separate
        parquet file and returns the folder-like prefix path you can treat as a dataset.
        (This avoids expensive read-append cycles.)
        """
        if not chunksize:
            df = self.read_sql(query, params=params)
            df.to_parquet(parquet_path, index=False)
            return parquet_path

        # Chunked dataset write: flights.parquet -> flights_part000.parquet, etc.
        base, ext = os.path.splitext(parquet_path)
        i = 0
        for chunk in self.read_sql(query, params=params, chunksize=chunksize):
            part_path = f"{base}_part{i:03d}.parquet"
            chunk.to_parquet(part_path, index=False)
            i += 1

        return f"{base}_part*.parquet"

    def save_table_as_parquet(
        self,
        schema: str,
        table: str,
        parquet_path: str,
        *,
        limit: Optional[int] = None,
        where: Optional[str] = None,
        chunksize: Optional[int] = None,
    ) -> str:
        """
        Save (part of) a table to Parquet.
        """
        sql = f"SELECT * FROM {schema}.{table}"
        if where:
            sql += f" WHERE {where}"
        if limit is not None:
            sql += f" FETCH FIRST {int(limit)} ROWS ONLY"
        return self.save_query_as_parquet(sql, parquet_path, chunksize=chunksize)

    # -------------------------
    # Convenience
    # -------------------------
    def head(self, schema: str, table: str, n: int = 5) -> pd.DataFrame:
        """
        Shortcut for sample_table.
        """
        return self.sample_table(schema=schema, table=table, n=n)
