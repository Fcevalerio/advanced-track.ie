from db2_connector import DB2Connector

connector = DB2Connector()

# Test total revenue query
print("Testing total_revenue query:")
result = connector.get_total_revenue()
print("Columns:", result.columns.tolist())
print("Data:\n", result)
print()

# Test other queries
print("Testing load_factor query:")
result = connector.get_load_factor()
print("Columns:", result.columns.tolist())
print("First row:\n", result.head(1))
