# advanced-track.ie

IE's MBDS program for advanced track

## Database Connection Guide

This guide explains how to set up your Python environment and connect to the IBM DB2 database used in this project.

## 1. Required Libraries

The project relies on a specific set of Python libraries defined in `pyproject.toml`.

### Core Data & Analysis

* **`pandas`**: For data manipulation and analysis. Used to load query results into DataFrames.
* **`numpy`**: Fundamental package for scientific computing.
* **`scikit-learn`**: Machine learning library.
* **`plotly`**: For interactive graphing and visualization.

### Database Connectivity

* **`sqlalchemy`**: The Python SQL Toolkit and Object Relational Mapper. It provides the core interface for connecting to the database.
* **`ibm-db-sa`**: The SQLAlchemy adapter for IBM DB2. This allows SQLAlchemy to communicate specifically with DB2 databases.
  * *Note: This automatically installs the low-level `ibm_db` driver.*
* **`pyodbc`**: A standard ODBC driver (included for compatibility/alternative connection methods).
* **`duckdb`**: An in-process SQL OLAP database management system. Used here to perform fast analytical queries on local Pandas DataFrames.

### Utilities

* **`python-dotenv`**: For managing environment variables (e.g., keeping credentials secure).
* **`azure-identity`**: For Azure authentication support.

## 2. Environment Setup

This project uses `uv` for dependency management.

1. **Install uv**:
    If you don't have `uv` installed, follow the instructions in the [official documentation](https://docs.astral.sh/uv/getting-started/installation/).

    Quick install for macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Install Dependencies**:
    Run the following command in your terminal to create the virtual environment and install all required packages:
        ```bash
        uv sync
        ```

3. **Activate Environment**:
```bash
source .venv/bin/activate
```

## 3. Connecting to the Database

We use **SQLAlchemy** to establish the connection. The connection string follows the standard URL format for the `ibm_db_sa` dialect.

### Connection String Format

```
db2+ibm_db://<username>:<password>@<host>:<port>/<database>
```

### Python Code Example

Here is how to connect and run a query, based on `test_connection.ipynb`.

#### Step 1: Create the Engine

```python
from sqlalchemy import create_engine

# Replace with your actual credentials
connection_string = "db2+ibm_db://<username>:<password>@52.211.123.34:25010/IEMASTER"

engine = create_engine(connection_string)
```

#### Step 2: Querying with Pandas

The most efficient way to retrieve data for analysis is using `pandas.read_sql`.

```python
import pandas as pd

query = "SELECT * FROM IEPLANE.FLIGHTS FETCH FIRST 10 ROWS ONLY"
df = pd.read_sql(query, engine)

print(df.head())
```

## ATT Project Instructions

Now you have access to the data through pandas, you should follow these steps.

1. Create a python class to connect to the database and fetch data.

    * In order to connect, create an `env` file to store your credentials securely and use `python-dotenv` to load them into your connector class.
    * This class should have methods to execute queries and return data as pandas DataFrames.
    * Include tests to verify the connection and data retrieval.

2. With the connection ready, use streamlit to build an interactive dashboard.

    * Use plotly for visualizations.
    * Implement filters and interactive elements to explore the data.

3. Deliver your project by:

    * Forking this repository.
    * Committing your code and pushing it to your fork.
    * Sharing the link to your forked repository with all necessary instructions to run your project

## 4. Troubleshooting

* **`NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:db2.ibm_db`**:
    This means the `ibm-db-sa` library is missing. Ensure it is in your `pyproject.toml` and you have run `uv sync`.

* **Connection Timeouts**:
    Ensure you are connected to the internet and that the firewall allows traffic to port `25010`.
