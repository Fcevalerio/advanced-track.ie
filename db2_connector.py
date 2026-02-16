import os
import pandas as pd
from dotenv import load_dotenv
from typing import Optional
import numpy as np
from datetime import datetime, timedelta
import ibm_db

# Load environment variables from .env file
load_dotenv()


class DB2Connector:
    """
    A class to connect to IBM DB2 database and fetch airline data.
    Falls back to mock data if connection fails.
    """

    def __init__(self):
        """Initialize the DB2 connector with database credentials from .env file."""
        self.username = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST", "52.211.123.34")
        self.port = os.getenv("DB_PORT", "25010")
        self.database = os.getenv("DB_NAME", "IEMASTER")
        self.use_mock = False
        self.connection = None
        self.test_connection()

    def test_connection(self) -> bool:
        """Test the database connection using IBM DB2 driver, fall back to mock data if failed."""
        try:
            # Try to connect using IBM DB2 driver
            connection_string = f"DATABASE={self.database};HOSTNAME={self.host};PORT={self.port};PROTOCOL=TCPIP;UID={self.username};PWD={self.password};"
            self.connection = ibm_db.connect(connection_string, "", "")
            stmt = ibm_db.exec_immediate(self.connection, "SELECT 1 FROM SYSIBM.SYSDUMMY1")
            ibm_db.fetch_row(stmt)
            print("✓ Connected to IBM DB2 database!")
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            print("⚠️ Falling back to mock data mode - all features available with sample data!")
            self.use_mock = True
            return False

    def _get_connection(self):
        """Get or create database connection."""
        if self.connection is None:
            try:
                connection_string = f"DATABASE={self.database};HOSTNAME={self.host};PORT={self.port};PROTOCOL=TCPIP;UID={self.username};PWD={self.password};"
                self.connection = ibm_db.connect(connection_string, "", "")
            except Exception as e:
                print(f"Error creating connection: {e}")
                self.use_mock = True
        return self.connection
    
    # ===== MOCK DATA METHODS =====
    
    def _get_mock_total_revenue(self) -> pd.DataFrame:
        """Return mock total revenue data."""
        return pd.DataFrame({"total_revenue": [15750000.00]})

    def _get_mock_revenue_by_route(self) -> pd.DataFrame:
        """Return mock revenue by route."""
        return pd.DataFrame({
            "ROUTE_ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "origin": ["JFK", "LAX", "ORD", "DFW", "ATL", "DEN", "SFO", "MIA", "BOS", "LAS"],
            "destination": ["LAX", "JFK", "MIA", "LAX", "JFK", "LAX", "LAX", "NYC", "LAX", "LAS"],
            "total_revenue": [2500000, 2200000, 1800000, 1650000, 1500000, 1400000, 1300000, 1200000, 1100000, 1000000],
            "ticket_count": [5000, 4400, 3600, 3300, 3000, 2800, 2600, 2400, 2200, 2000],
            "avg_ticket_price": [500, 500, 500, 500, 500, 500, 500, 500, 500, 500],
        })

    def _get_mock_load_factor(self) -> pd.DataFrame:
        """Return mock load factor data."""
        np.random.seed(42)
        flights = 200
        return pd.DataFrame({
            "FLIGHT_ID": range(1, flights + 1),
            "origin": np.random.choice(["JFK", "LAX", "ORD", "DFW", "ATL"], flights),
            "destination": np.random.choice(["LAX", "JFK", "MIA", "ORD", "DEN"], flights),
            "CAPACITY": np.random.choice([150, 180, 200, 250], flights),
            "passengers_booked": np.random.randint(100, 250, flights),
            "load_factor": np.random.uniform(65, 95, flights),
        })

    def _get_mock_fleet_utilization(self) -> pd.DataFrame:
        """Return mock fleet utilization."""
        np.random.seed(42)
        return pd.DataFrame({
            "AIRPLANE_ID": range(1, 31),
            "MODEL": np.random.choice(["Boeing 747", "Boeing 787", "Airbus A380", "Airbus A350"], 30),
            "REGISTRATION_NUMBER": [f"N{1000+i}" for i in range(30)],
            "TOTAL_FLIGHT_DISTANCE": np.random.randint(100000, 500000, 30),
            "FLIGHT_HOURS": np.random.randint(1000, 5000, 30),
            "FUEL_GALLONS_HOUR": np.random.uniform(4000, 8000, 30),
            "total_flights": np.random.randint(50, 300, 30),
            "MAINTENANCE_LAST_ACHECK": np.random.randint(0, 1000, 30),
            "MAINTENANCE_TAKEOFFS": np.random.randint(300, 950, 30),
        })

    def _get_mock_fuel_efficiency(self) -> pd.DataFrame:
        """Return mock fuel efficiency data."""
        return pd.DataFrame({
            "MODEL": ["Boeing 787", "Airbus A350", "Boeing 747", "Airbus A380"],
            "aircraft_count": [12, 8, 10, 5],
            "avg_fuel_consumption": [5100, 5300, 6500, 7000],
            "avg_distance": [450000, 420000, 380000, 400000],
            "avg_flight_hours": [4200, 3800, 3500, 3700],
        })

    def _get_mock_maintenance_alerts(self) -> pd.DataFrame:
        """Return mock maintenance alerts."""
        return pd.DataFrame({
            "AIRPLANE_ID": [1, 5, 8, 12, 15, 18],
            "MODEL": ["Boeing 747", "Airbus A380", "Boeing 787", "Airbus A350", "Boeing 747", "Airbus A380"],
            "REGISTRATION_NUMBER": ["N1001", "N1005", "N1008", "N1012", "N1015", "N1018"],
            "MAINTENANCE_TAKEOFFS": [950, 900, 850, 800, 750, 700],
            "maintenance_status": ["CRITICAL", "CRITICAL", "HIGH", "HIGH", "MEDIUM", "MEDIUM"],
        })

    def _get_mock_passenger_demographics(self) -> pd.DataFrame:
        """Return mock passenger demographics."""
        return pd.DataFrame({
            "GENDER": ["M", "F"],
            "passenger_count": [52000, 48000],
            "avg_age": [42.5, 38.2],
            "min_age": [18, 18],
            "max_age": [82, 85],
        })

    def _get_mock_hr_metrics(self) -> pd.DataFrame:
        """Return mock HR metrics."""
        return pd.DataFrame({
            "DEPARTMENT_ID": [1, 2, 3, 4],
            "DEPARTMENT_NAME": ["Flight Operations", "Maintenance", "Customer Service", "Administration"],
            "headcount": [350, 450, 280, 120],
            "total_salary": [12600000, 13500000, 7840000, 4200000],
            "avg_salary": [36000, 30000, 28000, 35000],
        })

    def _get_mock_route_network(self) -> pd.DataFrame:
        """Return mock route network data."""
        np.random.seed(42)
        return pd.DataFrame({
            "ROUTE_ID": range(1, 21),
            "origin_id": range(1, 21),
            "origin": np.random.choice(["JFK", "LAX", "ORD", "DFW", "ATL"], 20),
            "origin_lat": np.random.uniform(25, 45, 20),
            "origin_lon": np.random.uniform(-125, -70, 20),
            "destination_id": range(21, 41),
            "destination": np.random.choice(["LAX", "JFK", "MIA", "ORD", "DEN"], 20),
            "destination_lat": np.random.uniform(25, 45, 20),
            "destination_lon": np.random.uniform(-125, -70, 20),
            "flight_count": np.random.randint(50, 300, 20),
            "passenger_count": np.random.randint(5000, 50000, 20),
        })

    def _get_mock_financial_trends(self) -> pd.DataFrame:
        """Return mock financial trends."""
        np.random.seed(42)
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        return pd.DataFrame({
            "flight_date": dates,
            "ticket_count": np.random.randint(200, 500, 30),
            "daily_revenue": np.random.randint(500000, 1500000, 30),
            "avg_ticket_price": np.random.uniform(400, 600, 30),
        })

    def get_total_revenue(self) -> pd.DataFrame:
        """Fetch total revenue from tickets."""
        if self.use_mock:
            return self._get_mock_total_revenue()
        try:
            query = "SELECT SUM(total_amount) as total_revenue FROM IEPLANE.TICKETS"
            return pd.read_sql(query, self._get_connection())
        except Exception as e:
            print(f"Error fetching total revenue: {e}")
            self.use_mock = True
            return self._get_mock_total_revenue()

    def get_revenue_by_route(self) -> pd.DataFrame:
        """Fetch revenue aggregated by route."""
        if self.use_mock:
            return self._get_mock_revenue_by_route()
        try:
            query = """
            SELECT 
                r.ROUTE_ID,
                a1.AIRPORT_NAME as origin,
                a2.AIRPORT_NAME as destination,
                SUM(t.total_amount) as total_revenue,
                COUNT(t.TICKET_ID) as ticket_count,
                AVG(t.total_amount) as avg_ticket_price
            FROM IEPLANE.ROUTES r
            JOIN IEPLANE.AIRPORTS a1 ON r.ORIGIN_AIRPORT_ID = a1.AIRPORT_ID
            JOIN IEPLANE.AIRPORTS a2 ON r.DESTINATION_AIRPORT_ID = a2.AIRPORT_ID
            LEFT JOIN IEPLANE.FLIGHTS f ON r.ROUTE_ID = f.ROUTE_ID
            LEFT JOIN IEPLANE.TICKETS t ON f.FLIGHT_ID = t.FLIGHT_ID
            GROUP BY r.ROUTE_ID, a1.AIRPORT_NAME, a2.AIRPORT_NAME
            ORDER BY total_revenue DESC
            """
            return pd.read_sql(query, self._get_connection())
        except Exception as e:
            print(f"Error fetching revenue by route: {e}")
            self.use_mock = True
            return self._get_mock_revenue_by_route()

    def get_load_factor(self) -> pd.DataFrame:
        """Calculate load factor (percentage of seats filled) by flight."""
        if self.use_mock:
            return self._get_mock_load_factor()
        try:
            query = """
            SELECT 
                f.FLIGHT_ID,
                r.ROUTE_ID,
                a1.AIRPORT_NAME as origin,
                a2.AIRPORT_NAME as destination,
                ap.CAPACITY,
                COUNT(t.TICKET_ID) as passengers_booked,
                ROUND(FLOAT(COUNT(t.TICKET_ID)) / ap.CAPACITY * 100, 2) as load_factor
            FROM IEPLANE.FLIGHTS f
            JOIN IEPLANE.ROUTES r ON f.ROUTE_ID = r.ROUTE_ID
            JOIN IEPLANE.AIRPORTS a1 ON r.ORIGIN_AIRPORT_ID = a1.AIRPORT_ID
            JOIN IEPLANE.AIRPORTS a2 ON r.DESTINATION_AIRPORT_ID = a2.AIRPORT_ID
            JOIN IEPLANE.AIRPLANES ap ON f.AIRPLANE_ID = ap.AIRPLANE_ID
            LEFT JOIN IEPLANE.TICKETS t ON f.FLIGHT_ID = t.FLIGHT_ID
            GROUP BY f.FLIGHT_ID, r.ROUTE_ID, a1.AIRPORT_NAME, a2.AIRPORT_NAME, ap.CAPACITY
            ORDER BY load_factor DESC
            """
            return pd.read_sql(query, self._get_connection())
        except Exception as e:
            print(f"Error fetching load factor: {e}")
            self.use_mock = True
            return self._get_mock_load_factor()

    def get_fleet_utilization(self) -> pd.DataFrame:
        """Fetch fleet utilization metrics."""
        if self.use_mock:
            return self._get_mock_fleet_utilization()
        try:
            query = """
            SELECT 
                ap.AIRPLANE_ID,
                ap.MODEL,
                ap.REGISTRATION_NUMBER,
                ap.TOTAL_FLIGHT_DISTANCE,
                ap.FLIGHT_HOURS,
                ap.FUEL_GALLONS_HOUR,
                COUNT(f.FLIGHT_ID) as total_flights,
                ap.MAINTENANCE_LAST_ACHECK,
                ap.MAINTENANCE_TAKEOFFS
            FROM IEPLANE.AIRPLANES ap
            LEFT JOIN IEPLANE.FLIGHTS f ON ap.AIRPLANE_ID = f.AIRPLANE_ID
            GROUP BY ap.AIRPLANE_ID, ap.MODEL, ap.REGISTRATION_NUMBER, 
                     ap.TOTAL_FLIGHT_DISTANCE, ap.FLIGHT_HOURS, ap.FUEL_GALLONS_HOUR,
                     ap.MAINTENANCE_LAST_ACHECK, ap.MAINTENANCE_TAKEOFFS
            ORDER BY ap.TOTAL_FLIGHT_DISTANCE DESC
            """
            return pd.read_sql(query, self._get_connection())
        except Exception as e:
            print(f"Error fetching fleet utilization: {e}")
            self.use_mock = True
            return self._get_mock_fleet_utilization()

    def get_fuel_efficiency(self) -> pd.DataFrame:
        """Fetch fuel efficiency leaderboard by aircraft model."""
        if self.use_mock:
            return self._get_mock_fuel_efficiency()
        try:
            query = """
            SELECT 
                ap.MODEL,
                COUNT(DISTINCT ap.AIRPLANE_ID) as aircraft_count,
                AVG(ap.FUEL_GALLONS_HOUR) as avg_fuel_consumption,
                AVG(ap.TOTAL_FLIGHT_DISTANCE) as avg_distance,
                AVG(ap.FLIGHT_HOURS) as avg_flight_hours
            FROM IEPLANE.AIRPLANES ap
            GROUP BY ap.MODEL
            ORDER BY avg_fuel_consumption ASC
            """
            return pd.read_sql(query, self._get_connection())
        except Exception as e:
            print(f"Error fetching fuel efficiency: {e}")
            self.use_mock = True
            return self._get_mock_fuel_efficiency()

    def get_maintenance_alerts(self) -> pd.DataFrame:
        """Fetch aircraft approaching maintenance thresholds."""
        if self.use_mock:
            return self._get_mock_maintenance_alerts()
        try:
            query = """
            SELECT 
                ap.AIRPLANE_ID,
                ap.MODEL,
                ap.REGISTRATION_NUMBER,
                ap.MAINTENANCE_LAST_ACHECK,
                ap.MAINTENANCE_TAKEOFFS,
                CASE 
                    WHEN ap.MAINTENANCE_TAKEOFFS >= 900 THEN 'CRITICAL'
                    WHEN ap.MAINTENANCE_TAKEOFFS >= 700 THEN 'HIGH'
                    WHEN ap.MAINTENANCE_TAKEOFFS >= 500 THEN 'MEDIUM'
                    ELSE 'LOW'
                END as maintenance_status
            FROM IEPLANE.AIRPLANES ap
            WHERE ap.MAINTENANCE_TAKEOFFS >= 500
            ORDER BY ap.MAINTENANCE_TAKEOFFS DESC
            """
            return pd.read_sql(query, self._get_connection())
        except Exception as e:
            print(f"Error fetching maintenance alerts: {e}")
            self.use_mock = True
            return self._get_mock_maintenance_alerts()

    def get_passenger_demographics(self) -> pd.DataFrame:
        """Fetch passenger demographics (age and gender distribution)."""
        if self.use_mock:
            return self._get_mock_passenger_demographics()
        try:
            query = """
            SELECT 
                GENDER,
                COUNT(*) as passenger_count,
                ROUND(AVG(AGE), 1) as avg_age,
                MIN(AGE) as min_age,
                MAX(AGE) as max_age
            FROM IEPLANE.PASSENGERS
            GROUP BY GENDER
            """
            return pd.read_sql(query, self._get_connection())
        except Exception as e:
            print(f"Error fetching passenger demographics: {e}")
            self.use_mock = True
            return self._get_mock_passenger_demographics()

    def get_hr_metrics(self) -> pd.DataFrame:
        """Fetch HR metrics (headcount and budget by department)."""
        if self.use_mock:
            return self._get_mock_hr_metrics()
        try:
            query = """
            SELECT 
                d.DEPARTMENT_ID,
                d.DEPARTMENT_NAME,
                COUNT(e.EMPLOYEE_ID) as headcount,
                SUM(e.SALARY) as total_salary,
                AVG(e.SALARY) as avg_salary
            FROM IEPLANE.DEPARTMENTS d
            LEFT JOIN IEPLANE.EMPLOYEES e ON d.DEPARTMENT_ID = e.DEPARTMENT_ID
            GROUP BY d.DEPARTMENT_ID, d.DEPARTMENT_NAME
            ORDER BY total_salary DESC
            """
            return pd.read_sql(query, self._get_connection())
        except Exception as e:
            print(f"Error fetching HR metrics: {e}")
            self.use_mock = True
            return self._get_mock_hr_metrics()

    def get_route_network(self) -> pd.DataFrame:
        """Fetch route network data with airport coordinates for heatmap."""
        if self.use_mock:
            return self._get_mock_route_network()
        try:
            query = """
            SELECT 
                r.ROUTE_ID,
                a1.AIRPORT_ID as origin_id,
                a1.AIRPORT_NAME as origin,
                a1.LATITUDE as origin_lat,
                a1.LONGITUDE as origin_lon,
                a2.AIRPORT_ID as destination_id,
                a2.AIRPORT_NAME as destination,
                a2.LATITUDE as destination_lat,
                a2.LONGITUDE as destination_lon,
                COUNT(f.FLIGHT_ID) as flight_count,
                SUM(CASE WHEN t.TICKET_ID IS NOT NULL THEN 1 ELSE 0 END) as passenger_count
            FROM IEPLANE.ROUTES r
            JOIN IEPLANE.AIRPORTS a1 ON r.ORIGIN_AIRPORT_ID = a1.AIRPORT_ID
            JOIN IEPLANE.AIRPORTS a2 ON r.DESTINATION_AIRPORT_ID = a2.AIRPORT_ID
            LEFT JOIN IEPLANE.FLIGHTS f ON r.ROUTE_ID = f.ROUTE_ID
            LEFT JOIN IEPLANE.TICKETS t ON f.FLIGHT_ID = t.FLIGHT_ID
            GROUP BY r.ROUTE_ID, a1.AIRPORT_ID, a1.AIRPORT_NAME, a1.LATITUDE, a1.LONGITUDE,
                     a2.AIRPORT_ID, a2.AIRPORT_NAME, a2.LATITUDE, a2.LONGITUDE
            ORDER BY flight_count DESC
            """
            return pd.read_sql(query, self._get_connection())
        except Exception as e:
            print(f"Error fetching route network: {e}")
            self.use_mock = True
            return self._get_mock_route_network()

    def get_financial_trends(self) -> pd.DataFrame:
        """Fetch revenue trends over time."""
        if self.use_mock:
            return self._get_mock_financial_trends()
        try:
            query = """
            SELECT 
                DATE(f.DEPARTURE_TIME) as flight_date,
                COUNT(DISTINCT t.TICKET_ID) as ticket_count,
                SUM(t.total_amount) as daily_revenue,
                AVG(t.total_amount) as avg_ticket_price
            FROM IEPLANE.FLIGHTS f
            LEFT JOIN IEPLANE.TICKETS t ON f.FLIGHT_ID = t.FLIGHT_ID
            GROUP BY DATE(f.DEPARTURE_TIME)
            ORDER BY flight_date DESC
            """
            return pd.read_sql(query, self._get_connection())
        except Exception as e:
            print(f"Error fetching financial trends: {e}")
            self.use_mock = True
            return self._get_mock_financial_trends()

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute a custom query and return as DataFrame."""
        try:
            return pd.read_sql(query, self._get_connection())
        except Exception as e:
            print(f"Error executing query: {e}")
            self.use_mock = True
            return pd.DataFrame()


if __name__ == "__main__":
    connector = DB2Connector()
    print("Testing IBM DB2 connection...")
    if connector.test_connection():
        print("✓ Connection successful!")
    else:
        print("✗ Connection failed!")
