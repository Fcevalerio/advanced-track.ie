import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from db2_connector import DB2Connector


class TestDB2Connector(unittest.TestCase):
    """Unit tests for DB2Connector class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_credentials = {
            "DB_USERNAME": "test_user",
            "DB_PASSWORD": "test_password",
            "DB_HOST": "52.211.123.34",
            "DB_PORT": "25010",
            "DB_NAME": "IEMASTER",
        }

    @patch.dict("os.environ", {**{"DB_USERNAME": "test_user", "DB_PASSWORD": "test_password"}, **{}})
    def test_connection(self):
        """Test the database connection."""
        with patch("db2_connector.create_engine") as mock_engine:
            mock_connection = MagicMock()
            mock_engine.return_value.connect.return_value.__enter__.return_value = mock_connection
            mock_connection.execute.return_value.fetchone.return_value = (1,)

            connector = DB2Connector()
            result = connector.test_connection()
            self.assertTrue(result)

    @patch.dict("os.environ", {"DB_USERNAME": "test_user", "DB_PASSWORD": "test_password"})
    def test_missing_credentials(self):
        """Test initialization with missing credentials."""
        with patch.dict("os.environ", {"DB_USERNAME": "", "DB_PASSWORD": ""}, clear=True):
            with self.assertRaises(ValueError):
                DB2Connector()

    @patch.dict("os.environ", {"DB_USERNAME": "test_user", "DB_PASSWORD": "test_password"})
    @patch("db2_connector.pd.read_sql")
    def test_get_total_revenue(self, mock_read_sql):
        """Test fetching total revenue."""
        mock_data = {"total_revenue": [150000.00]}
        mock_read_sql.return_value = pd.DataFrame(mock_data)

        with patch("db2_connector.create_engine"):
            connector = DB2Connector()
            result = connector.get_total_revenue()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    @patch.dict("os.environ", {"DB_USERNAME": "test_user", "DB_PASSWORD": "test_password"})
    @patch("db2_connector.pd.read_sql")
    def test_get_revenue_by_route(self, mock_read_sql):
        """Test fetching revenue by route."""
        mock_data = {
            "ROUTE_ID": [1, 2],
            "origin": ["JFK", "LAS"],
            "destination": ["LAX", "ORD"],
            "total_revenue": [250000.00, 180000.00],
            "ticket_count": [500, 360],
        }
        mock_read_sql.return_value = pd.DataFrame(mock_data)

        with patch("db2_connector.create_engine"):
            connector = DB2Connector()
            result = connector.get_revenue_by_route()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)

    @patch.dict("os.environ", {"DB_USERNAME": "test_user", "DB_PASSWORD": "test_password"})
    @patch("db2_connector.pd.read_sql")
    def test_get_load_factor(self, mock_read_sql):
        """Test fetching load factor calculations."""
        mock_data = {
            "FLIGHT_ID": [1, 2],
            "origin": ["JFK", "LAS"],
            "destination": ["LAX", "ORD"],
            "CAPACITY": [180, 150],
            "passengers_booked": [150, 130],
            "load_factor": [83.33, 86.67],
        }
        mock_read_sql.return_value = pd.DataFrame(mock_data)

        with patch("db2_connector.create_engine"):
            connector = DB2Connector()
            result = connector.get_load_factor()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("load_factor", result.columns)

    @patch.dict("os.environ", {"DB_USERNAME": "test_user", "DB_PASSWORD": "test_password"})
    @patch("db2_connector.pd.read_sql")
    def test_get_fleet_utilization(self, mock_read_sql):
        """Test fetching fleet utilization metrics."""
        mock_data = {
            "AIRPLANE_ID": [1, 2],
            "MODEL": ["Boeing 747", "Airbus A380"],
            "REGISTRATION_NUMBER": ["N1001", "N1002"],
            "TOTAL_FLIGHT_DISTANCE": [500000, 600000],
            "FLIGHT_HOURS": [2000, 2500],
            "total_flights": [150, 180],
        }
        mock_read_sql.return_value = pd.DataFrame(mock_data)

        with patch("db2_connector.create_engine"):
            connector = DB2Connector()
            result = connector.get_fleet_utilization()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("MODEL", result.columns)

    @patch.dict("os.environ", {"DB_USERNAME": "test_user", "DB_PASSWORD": "test_password"})
    @patch("db2_connector.pd.read_sql")
    def test_get_fuel_efficiency(self, mock_read_sql):
        """Test fetching fuel efficiency leaderboard."""
        mock_data = {
            "MODEL": ["Boeing 787", "Airbus A350"],
            "aircraft_count": [12, 8],
            "avg_fuel_consumption": [5000, 5200],
        }
        mock_read_sql.return_value = pd.DataFrame(mock_data)

        with patch("db2_connector.create_engine"):
            connector = DB2Connector()
            result = connector.get_fuel_efficiency()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    @patch.dict("os.environ", {"DB_USERNAME": "test_user", "DB_PASSWORD": "test_password"})
    @patch("db2_connector.pd.read_sql")
    def test_get_maintenance_alerts(self, mock_read_sql):
        """Test fetching maintenance alerts."""
        mock_data = {
            "AIRPLANE_ID": [1, 2],
            "MODEL": ["Boeing 747", "Airbus A380"],
            "MAINTENANCE_TAKEOFFS": [950, 750],
            "maintenance_status": ["CRITICAL", "HIGH"],
        }
        mock_read_sql.return_value = pd.DataFrame(mock_data)

        with patch("db2_connector.create_engine"):
            connector = DB2Connector()
            result = connector.get_maintenance_alerts()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("maintenance_status", result.columns)

    @patch.dict("os.environ", {"DB_USERNAME": "test_user", "DB_PASSWORD": "test_password"})
    @patch("db2_connector.pd.read_sql")
    def test_get_passenger_demographics(self, mock_read_sql):
        """Test fetching passenger demographics."""
        mock_data = {
            "GENDER": ["M", "F"],
            "passenger_count": [5000, 4500],
            "avg_age": [42.5, 38.2],
        }
        mock_read_sql.return_value = pd.DataFrame(mock_data)

        with patch("db2_connector.create_engine"):
            connector = DB2Connector()
            result = connector.get_passenger_demographics()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)

    @patch.dict("os.environ", {"DB_USERNAME": "test_user", "DB_PASSWORD": "test_password"})
    @patch("db2_connector.pd.read_sql")
    def test_get_hr_metrics(self, mock_read_sql):
        """Test fetching HR metrics."""
        mock_data = {
            "DEPARTMENT_NAME": ["Flight Crew", "Maintenance", "Admin"],
            "headcount": [150, 200, 50],
            "total_salary": [4500000, 5000000, 2000000],
        }
        mock_read_sql.return_value = pd.DataFrame(mock_data)

        with patch("db2_connector.create_engine"):
            connector = DB2Connector()
            result = connector.get_hr_metrics()

        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    @patch.dict("os.environ", {"DB_USERNAME": "test_user", "DB_PASSWORD": "test_password"})
    @patch("db2_connector.pd.read_sql")
    def test_execute_query(self, mock_read_sql):
        """Test executing a custom query."""
        mock_data = {"result": [1, 2, 3]}
        mock_read_sql.return_value = pd.DataFrame(mock_data)

        with patch("db2_connector.create_engine"):
            connector = DB2Connector()
            result = connector.execute_query("SELECT * FROM TEST_TABLE")

        self.assertIsInstance(result, pd.DataFrame)
        mock_read_sql.assert_called_once()


if __name__ == "__main__":
    unittest.main()
