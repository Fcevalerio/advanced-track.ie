import os
import pandas as pd
from dotenv import load_dotenv
import site

clidriver_bin = None
for base in site.getsitepackages():
    candidate = os.path.join(base, "clidriver", "bin")
    if os.path.isdir(candidate):
        clidriver_bin = candidate
        break

if not clidriver_bin:
    raise RuntimeError("clidriver\\bin not found under site-packages (ibm_db install may be incomplete)")
import os
import pandas as pd
from dotenv import load_dotenv
import site

clidriver_bin = None
for base in site.getsitepackages():
    candidate = os.path.join(base, "clidriver", "bin")
    if os.path.isdir(candidate):
        clidriver_bin = candidate
        break

if not clidriver_bin:
    raise RuntimeError("clidriver\\bin not found under site-packages (ibm_db install may be incomplete)")

os.add_dll_directory(clidriver_bin)

import ibm_db

load_dotenv()


class DB2Connector:
    """A class to connect to IBM DB2 database and fetch airline data."""

    def __init__(self):
        """Initialize the DB2 connector with database credentials from .env file."""
        self.username = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST", "52.211.123.34")
        self.port = os.getenv("DB_PORT", "25010")
        self.database = os.getenv("DB_NAME", "IEMASTER")
        self.connection = None
        self.test_connection()

    def test_connection(self) -> bool:
        """Test the database connection using IBM DB2 driver."""
        try:
            connection_string = f"DATABASE={self.database};HOSTNAME={self.host};PORT={self.port};PROTOCOL=TCPIP;UID={self.username};PWD={self.password};"
            self.connection = ibm_db.connect(connection_string, "", "")
            stmt = ibm_db.exec_immediate(self.connection, "SELECT 1 FROM SYSIBM.SYSDUMMY1")
            ibm_db.fetch_row(stmt)
            print("✓ Connected to IBM DB2 database!")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            raise

    def _get_connection(self):
        """Get or create database connection."""
        if self.connection is None:
            connection_string = f"DATABASE={self.database};HOSTNAME={self.host};PORT={self.port};PROTOCOL=TCPIP;UID={self.username};PWD={self.password};"
            self.connection = ibm_db.connect(connection_string, "", "")
        return self.connection

    def _execute_query(self, query: str) -> pd.DataFrame:
        """Execute query and return as DataFrame."""
        conn = self._get_connection()
        stmt = ibm_db.exec_immediate(conn, query)

        # Get column names
        col_names = []
        i = 0
        while True:
            try:
                name = ibm_db.field_name(stmt, i)
                if name is False:
                    break
                col_names.append(name)
                i += 1
            except:
                break

        # Fetch data
        rows = []
        while True:
            row = ibm_db.fetch_tuple(stmt)
            if not row:
                break
            rows.append(row)

        # Create DataFrame
        if rows:
            return pd.DataFrame(rows, columns=col_names)
        else:
            return pd.DataFrame()

    def get_total_revenue(self) -> pd.DataFrame:
        """Fetch total revenue from tickets."""
        query = """
        SELECT SUM(TOTAL_AMOUNT) as TOTAL_REVENUE
        FROM IEPLANE.TICKETS t
        """
        return self._execute_query(query)

    def get_revenue_by_route(self) -> pd.DataFrame:
        """Fetch revenue aggregated by route."""
        query = """
        SELECT 
            r.ROUTE_CODE,
            r.ORIGIN,
            r.DESTINATION,
            SUM(t.TOTAL_AMOUNT) as TOTAL_REVENUE,
            COUNT(t.TICKET_ID) as TICKET_COUNT,
            AVG(t.TOTAL_AMOUNT) as AVG_TICKET_PRICE
        FROM IEPLANE.ROUTES r
        LEFT JOIN IEPLANE.TICKETS t ON r.ROUTE_CODE = t.ROUTE_CODE
        GROUP BY r.ROUTE_CODE, r.ORIGIN, r.DESTINATION
        ORDER BY TOTAL_REVENUE DESC
        FETCH FIRST 100 ROWS ONLY
        """
        return self._execute_query(query)

    def get_load_factor(self) -> pd.DataFrame:
        """Calculate load factor by flight."""
        query = """
        SELECT 
            f.FLIGHT_ID,
            r.ROUTE_CODE,
            r.ORIGIN,
            r.DESTINATION,
            (a.SEATS_BUSINESS + a.SEATS_PREMIUM + a.SEATS_ECONOMY) as CAPACITY,
            COUNT(t.TICKET_ID) as PASSENGERS_BOOKED,
            ROUND(FLOAT(COUNT(t.TICKET_ID)) / (a.SEATS_BUSINESS + a.SEATS_PREMIUM + a.SEATS_ECONOMY) * 100, 2) as LOAD_FACTOR
        FROM IEPLANE.FLIGHTS f
        JOIN IEPLANE.ROUTES r ON f.ROUTE_CODE = r.ROUTE_CODE
        JOIN IEPLANE.AIRPLANES a ON f.AIRPLANE = a.AIRCRAFT_REGISTRATION
        LEFT JOIN IEPLANE.TICKETS t ON f.FLIGHT_ID = t.FLIGHT_ID
        GROUP BY f.FLIGHT_ID, r.ROUTE_CODE, r.ORIGIN, r.DESTINATION, a.SEATS_BUSINESS, a.SEATS_PREMIUM, a.SEATS_ECONOMY
        ORDER BY LOAD_FACTOR DESC
        FETCH FIRST 500 ROWS ONLY
        """
        return self._execute_query(query)

    def get_fleet_utilization(self) -> pd.DataFrame:
        """Fetch fleet utilization metrics."""
        query = """
        SELECT 
            a.AIRCRAFT_REGISTRATION,
            a.MODEL,
            a.SEATS_BUSINESS + a.SEATS_PREMIUM + a.SEATS_ECONOMY as TOTAL_SEATS,
            a.TOTAL_FLIGHT_DISTANCE,
            a.MAINTENANCE_FLIGHT_HOURS,
            a.FUEL_GALLONS_HOUR,
            COUNT(f.FLIGHT_ID) as TOTAL_FLIGHTS,
            a.MAINTENANCE_LAST_ACHECK,
            a.MAINTENANCE_TAKEOFFS
        FROM IEPLANE.AIRPLANES a
        LEFT JOIN IEPLANE.FLIGHTS f ON a.AIRCRAFT_REGISTRATION = f.AIRPLANE
        GROUP BY a.AIRCRAFT_REGISTRATION, a.MODEL, a.SEATS_BUSINESS, a.SEATS_PREMIUM, a.SEATS_ECONOMY,
                 a.TOTAL_FLIGHT_DISTANCE, a.MAINTENANCE_FLIGHT_HOURS, a.FUEL_GALLONS_HOUR,
                 a.MAINTENANCE_LAST_ACHECK, a.MAINTENANCE_TAKEOFFS
        ORDER BY a.TOTAL_FLIGHT_DISTANCE DESC
        """
        return self._execute_query(query)

    def get_fuel_efficiency(self) -> pd.DataFrame:
        """Fetch fuel efficiency leaderboard by aircraft model."""
        query = """
        SELECT 
            a.MODEL,
            COUNT(DISTINCT a.AIRCRAFT_REGISTRATION) as AIRCRAFT_COUNT,
            AVG(a.FUEL_GALLONS_HOUR) as AVG_FUEL_CONSUMPTION,
            AVG(a.TOTAL_FLIGHT_DISTANCE) as AVG_DISTANCE,
            AVG(a.MAINTENANCE_FLIGHT_HOURS) as AVG_FLIGHT_HOURS
        FROM IEPLANE.AIRPLANES a
        GROUP BY a.MODEL
        ORDER BY AVG_FUEL_CONSUMPTION ASC
        """
        return self._execute_query(query)

    def get_maintenance_alerts(self) -> pd.DataFrame:
        """Fetch aircraft approaching maintenance thresholds."""
        query = """
        SELECT 
            a.AIRCRAFT_REGISTRATION,
            a.MODEL,
            a.MAINTENANCE_LAST_ACHECK,
            a.MAINTENANCE_LAST_BCHECK,
            a.MAINTENANCE_TAKEOFFS,
            CASE 
                WHEN a.MAINTENANCE_TAKEOFFS >= 900 THEN 'CRITICAL'
                WHEN a.MAINTENANCE_TAKEOFFS >= 700 THEN 'HIGH'
                WHEN a.MAINTENANCE_TAKEOFFS >= 500 THEN 'MEDIUM'
                ELSE 'LOW'
            END as MAINTENANCE_STATUS
        FROM IEPLANE.AIRPLANES a
        WHERE a.MAINTENANCE_TAKEOFFS >= 500
        ORDER BY a.MAINTENANCE_TAKEOFFS DESC
        """
        return self._execute_query(query)

    def get_passenger_demographics(self) -> pd.DataFrame:
        """Fetch passenger demographics."""
        query = """
        SELECT 
            GENDER,
            COUNT(*) as PASSENGER_COUNT,
            ROUND(AVG(YEAR(CURRENT_DATE) - YEAR(BIRTH_DATE)), 1) as AVG_AGE,
            MIN(YEAR(CURRENT_DATE) - YEAR(BIRTH_DATE)) as MIN_AGE,
            MAX(YEAR(CURRENT_DATE) - YEAR(BIRTH_DATE)) as MAX_AGE
        FROM IEPLANE.PASSENGERS p
        GROUP BY GENDER
        """
        return self._execute_query(query)

    def get_hr_metrics(self) -> pd.DataFrame:
        """Fetch HR metrics by department."""
        query = """
        SELECT 
            d.DEPTNO,
            d.DEPTNAME,
            COUNT(e.EMPNO) as HEADCOUNT,
            SUM(e.SALARY) as TOTAL_SALARY,
            AVG(e.SALARY) as AVG_SALARY,
            d.BUDGET
        FROM IEPLANE.DEPARTMENT d
        LEFT JOIN IEPLANE.EMPLOYEE e ON d.DEPTNO = e.WORKDEPT
        GROUP BY d.DEPTNO, d.DEPTNAME, d.BUDGET
        ORDER BY TOTAL_SALARY DESC
        """
        return self._execute_query(query)

    def get_route_network(self) -> pd.DataFrame:
        """Fetch route network data with airport coordinates."""
        query = """
        SELECT 
            r.ROUTE_CODE,
            ao.IATA_CODE as ORIGIN_CODE,
            ao.AIRPORT as ORIGIN,
            ao.LATITUDE as ORIGIN_LAT,
            ao.LONGITUDE as ORIGIN_LON,
            ad.IATA_CODE as DESTINATION_CODE,
            ad.AIRPORT as DESTINATION,
            ad.LATITUDE as DESTINATION_LAT,
            ad.LONGITUDE as DESTINATION_LON,
            COUNT(f.FLIGHT_ID) as FLIGHT_COUNT,
            COUNT(DISTINCT t.TICKET_ID) as PASSENGER_COUNT
        FROM IEPLANE.ROUTES r
        JOIN IEPLANE.AIRPORTS ao ON r.ORIGIN = ao.IATA_CODE
        JOIN IEPLANE.AIRPORTS ad ON r.DESTINATION = ad.IATA_CODE
        LEFT JOIN IEPLANE.FLIGHTS f ON r.ROUTE_CODE = f.ROUTE_CODE
        LEFT JOIN IEPLANE.TICKETS t ON f.FLIGHT_ID = t.FLIGHT_ID
        GROUP BY r.ROUTE_CODE, ao.IATA_CODE, ao.AIRPORT, ao.LATITUDE, ao.LONGITUDE,
                 ad.IATA_CODE, ad.AIRPORT, ad.LATITUDE, ad.LONGITUDE
        ORDER BY FLIGHT_COUNT DESC
        FETCH FIRST 100 ROWS ONLY
        """
        return self._execute_query(query)

    def get_financial_trends(self) -> pd.DataFrame:
        """Fetch revenue trends over time."""
        query = """
        SELECT 
            DATE(f.DEPARTURE) as FLIGHT_DATE,
            COUNT(DISTINCT t.TICKET_ID) as TICKET_COUNT,
            SUM(t.TOTAL_AMOUNT) as DAILY_REVENUE,
            AVG(t.TOTAL_AMOUNT) as AVG_TICKET_PRICE
        FROM IEPLANE.FLIGHTS f
        LEFT JOIN IEPLANE.TICKETS t ON f.FLIGHT_ID = t.FLIGHT_ID
        GROUP BY DATE(f.DEPARTURE)
        ORDER BY FLIGHT_DATE DESC
        FETCH FIRST 100 ROWS ONLY
        """
        return self._execute_query(query)

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute custom query."""
        return self._execute_query(query)


if __name__ == "__main__":
    connector = DB2Connector()
    print("Testing IBM DB2 connection...")
    if connector.test_connection():
        print("✓ Connection successful!")
    else:
        print("✗ Connection failed!")

