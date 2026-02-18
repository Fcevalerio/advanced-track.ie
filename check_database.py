from db2_connector import DB2Connector

connector = DB2Connector()

# Get all tables
print("=" * 80)
print("TABLES IN IEPLANE SCHEMA")
print("=" * 80)
query_tables = "SELECT TABNAME FROM SYSCAT.TABLES WHERE TABSCHEMA = 'IEPLANE'"
tables = connector.execute_query(query_tables)
print(tables)

# Get all columns for each table
print("\n" + "=" * 80)
print("COLUMNS BY TABLE")
print("=" * 80)
query_cols = "SELECT TABNAME, COLNAME FROM SYSCAT.COLUMNS WHERE TABSCHEMA = 'IEPLANE' ORDER BY TABNAME, COLNO"
columns = connector.execute_query(query_cols)
print(columns)

# Export to CSV for easier viewing
columns.to_csv("database_schema.csv", index=False)
print("\n✓ Schema exported to database_schema.csv")
