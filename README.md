# SkyHigh Insights - Executive Airline Dashboard

An interactive web application to analyze and visualize airline operations data from an IBM DB2 database, built with Python, Streamlit, and Plotly.

## 📌 Project Overview

SkyHigh Insights provides a comprehensive Executive Command Center dashboard for analyzing the airline's financial health, operational efficiency, and fleet status. This project is part of the IE MBDS Advanced Tech Track program.

### Key Features

- **Executive Summary**: Real-time KPIs and high-level metrics
- **Financial Performance**: Revenue analysis by route and ticket class
- **Fleet Operations**: Aircraft utilization, fuel efficiency, and maintenance alerts
- **Route Network**: Geographic visualization of flight routes and passenger dynamics
- **HR Analytics**: Department headcount, budget distribution, and staffing metrics
- **Interactive Visualizations**: Built with Plotly for dynamic exploration
- **Real-time Data**: Fetches live data from IBM DB2 database

## 🎯 Key Pillars & KPIs

### 1. **Financial Performance (The Bottom Line)**
- Total Revenue: Aggregated from ticket sales
- Revenue per Available Seat Mile (RASM)
- Route Profitability analysis
- Ancillary Revenue breakdown

### 2. **Fleet Operations & Efficiency**
- Fleet Utilization metrics
- Maintenance Health with alert system
- Fuel Efficiency Leaderboard by aircraft model

### 3. **Commercial & Route Network**
- Load Factor: Percentage of seats filled
- Route Heatmap: Geographic visualization of busiest routes
- Passenger Demographics: Age and gender distribution

### 4. **Human Resources**
- Headcount & Budget by department
- Staffing Efficiency ratios
- Salary distribution analysis

## 🏗️ Technical Architecture

```
Data Pipeline:
1. Extraction: SQLAlchemy to pull raw data from IBM DB2
2. Transformation: Pandas for data manipulation and analysis
3. Visualization: Streamlit + Plotly for interactive dashboard
4. Security: python-dotenv for credential management
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- IBM DB2 database access
- Database credentials (username, password, host, port)
- Git (for version control)

### Installation

#### 1. Fork the Repository

1. Go to the original repository on GitHub
2. Click the Fork button (top-right corner)
3. Select your GitHub account as the destination

#### 2. Clone Your Fork

**Windows (PowerShell or Git Bash):**
```bash
git clone https://github.com/<your-github-username>/advanced-track.ie.git
cd advanced-track.ie
```

**macOS/Linux (Terminal):**
```bash
git clone https://github.com/<your-github-username>/advanced-track.ie.git
cd advanced-track.ie
```

#### 3. Set Up Environment

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

OR manually:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 4. Configure Database Credentials

1. Copy `.env.example` to `.env`:
   ```bash
   # Windows PowerShell:
   Copy-Item .env.example .env
   
   # Windows Command Prompt:
   copy .env.example .env
   
   # macOS/Linux:
   cp .env.example .env
   ```

2. Edit `.env` file with your IBM DB2 credentials:
   ```
   DB_USERNAME=your_username
   DB_PASSWORD=your_password
   DB_HOST=52.211.123.34
   DB_PORT=25010
   DB_NAME=IEMASTER
   ```

## 📊 Usage

### Running Tests

```bash
# Test the database connector
python -m unittest test_db2_connector.py -v
```

### Running the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Using the Connector Class Directly

```python
from db2_connector import DB2Connector
import pandas as pd

# Initialize connector
connector = DB2Connector()

# Test connection
if connector.test_connection():
    print("✓ Connected to IBM DB2!")

# Fetch total revenue
revenue = connector.get_total_revenue()
print(revenue)

# Get load factor analysis
load_factors = connector.get_load_factor()
print(load_factors.head())

# Analyze fleet utilization
fleet = connector.get_fleet_utilization()
print(fleet.head())

# Get passenger demographics
passengers = connector.get_passenger_demographics()
print(passengers)

# Get financial trends
trends = connector.get_financial_trends()
print(trends.head())
```

## 📁 Project Structure

```
advanced-track.ie/
├── db2_connector.py              # IBM DB2 connector class
├── dashboard.py                  # Streamlit dashboard application
├── test_db2_connector.py         # Unit tests for connector
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .env                          # Environment variables (create this)
├── .gitignore                    # Git ignore rules
├── setup.bat                     # Setup script for Windows
├── setup.sh                      # Setup script for macOS/Linux
├── project.json                  # Project configuration
├── PROJECT_PROPOSAL.md           # Project proposal document
└── README.md                     # This file
```

## 🧪 Testing

The project includes comprehensive unit tests for the database connector:

```bash
# Run all tests
python -m unittest discover

# Run specific test file
python -m unittest test_db2_connector.py -v

# Run with coverage
pip install coverage
coverage run -m unittest test_db2_connector.py
coverage report
```

### Test Coverage

- ✅ Database connection testing
- ✅ Revenue calculations
- ✅ Load factor analysis
- ✅ Fleet utilization metrics
- ✅ Fuel efficiency analysis
- ✅ Maintenance alerts
- ✅ Passenger demographics
- ✅ HR metrics retrieval
- ✅ Custom query execution

## 📊 Dashboard Pages

### 1. Executive Summary
- Total Revenue
- Average Load Factor
- Active Fleet Count
- Total Passengers
- Daily Revenue Trends

### 2. Financial Performance
- Revenue by Route
- Route Profitability Analysis
- Ticket Price Analysis by Route
- Revenue Distribution

### 3. Fleet Operations
- Fleet Utilization Metrics
- Fuel Efficiency Leaderboard
- Load Factor Analysis
- Maintenance Status Alerts

### 4. Route Network
- Route Heatmap (Geographic Distribution)
- Load Factor by Route
- Passenger Demographics (Gender, Age)

### 5. HR Analytics
- Headcount by Department
- Salary Budget Distribution
- Department Details
- Average Salary Analysis

## 🔐 Security Best Practices

- **No Data Storage**: All data is fetched from DB2 and not stored locally
- **Token Security**: Database credentials stored in `.env` file (never commit this)
- **Environment Variables**: Sensitive data managed through python-dotenv
- **Connection String**: Secure SQLAlchemy connection with ibm_db_sa

### Important: Never commit `.env`

The `.env` file is included in `.gitignore` to prevent accidentally uploading credentials. Always keep credentials secure and never share `.env` files.

## 🔗 Database Connection

### Connection String Format

```
db2+ibm_db://<username>:<password>@<host>:<port>/<database>
```

### Required Libraries

- **sqlalchemy**: SQL Toolkit and ORM
- **ibm-db-sa**: SQLAlchemy adapter for IBM DB2
- **pandas**: Data manipulation
- **numpy**: Scientific computing
- **streamlit**: Web app framework
- **plotly**: Interactive visualizations
- **python-dotenv**: Environment variable management

## 🛫 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app"
4. Select your repository and `dashboard.py`
5. Add secrets in advanced settings:
   ```
   DB_USERNAME = your_username
   DB_PASSWORD = your_password
   DB_HOST = 52.211.123.34
   DB_PORT = 25010
   DB_NAME = IEMASTER
   ```
6. Click "Deploy"

### Deploy to Heroku

1. Create `Procfile`:
   ```
   web: streamlit run --server.port $PORT --server.address 0.0.0.0 dashboard.py
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set DB_USERNAME=your_username
   heroku config:set DB_PASSWORD=your_password
   heroku config:set DB_HOST=52.211.123.34
   heroku config:set DB_PORT=25010
   heroku config:set DB_NAME=IEMASTER
   git push heroku main
   ```

## 📚 API Reference

### DB2Connector Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `test_connection()` | Test database connectivity | bool |
| `get_total_revenue()` | Total revenue from all tickets | DataFrame |
| `get_revenue_by_route()` | Revenue aggregated by route | DataFrame |
| `get_load_factor()` | Load factor for each flight | DataFrame |
| `get_fleet_utilization()` | Fleet metrics and utilization | DataFrame |
| `get_fuel_efficiency()` | Fuel consumption by aircraft model | DataFrame |
| `get_maintenance_alerts()` | Aircraft maintenance status | DataFrame |
| `get_passenger_demographics()` | Passenger demographics data | DataFrame |
| `get_hr_metrics()` | HR data by department | DataFrame |
| `get_route_network()` | Route network with coordinates | DataFrame |
| `get_financial_trends()` | Revenue trends over time | DataFrame |
| `execute_query(query)` | Execute custom SQL query | DataFrame |

All methods return Pandas DataFrames for easy data manipulation and analysis.

## 🐛 Troubleshooting

### Connection Issues

| Issue | Solution |
|-------|----------|
| `Missing DB_USERNAME or DB_PASSWORD` | Check `.env` file has correct credentials |
| `Connection timeout` | Verify internet connection and firewall allows port 25010 |
| `Plugin not found: ibm_db` | Run `pip install ibm-db-sa` |

### Data Issues

| Issue | Solution |
|-------|----------|
| Empty DataFrames | Verify database tables exist and have data |
| Slow queries | Check database server status and network |
| Special characters in column names | Use proper SQL quoting/escaping |

### Streamlit Issues

| Issue | Solution |
|-------|----------|
| Port 8501 already in use | Use `streamlit run dashboard.py --server.port 8502` |
| Module not found | Activate virtual environment and run `pip install -r requirements.txt` |

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Create a feature branch: `git checkout -b feature/amazing-feature`
2. Commit your changes: `git commit -m 'Add amazing feature'`
3. Push to your fork: `git push origin feature/amazing-feature`
4. Open a Pull Request

## 📞 Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section above
2. Review [IBM DB2 Documentation](https://www.ibm.com/docs/en/db2)
3. Check [Streamlit Documentation](https://docs.streamlit.io/)
4. Open an issue on the GitHub repository

## 🔗 Useful Resources

- [IBM DB2 Documentation](https://www.ibm.com/docs/en/db2)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Python dotenv Documentation](https://github.com/theskumar/python-dotenv)

## 📊 Next Steps

1. ✅ Set up environment and install dependencies
2. ✅ Configure database credentials in `.env`
3. ✅ Run tests to verify connection
4. ✅ Launch dashboard with `streamlit run dashboard.py`
5. 📊 Explore the dashboard and analyze data
6. 🚀 Deploy to production environment

## 👥 Team Collaboration

- **Repository Owner**: Hosts the forked repository
- **Collaborators**: Added to the fork via Settings > Collaborators
- **Branching Strategy**: Use feature branches for development
- **Pull Requests**: Review and merge before deploying to main

## 📅 Version History

- **v1.0.0** (February 2026): Initial release
  - Database connector with 11 query methods
  - Streamlit dashboard with 5 pages
  - Comprehensive unit tests
  - Full documentation

---

**Last Updated**: February 2026  
**Project Status**: Active Development  
**Maintainer**: IE MBDS Advanced Track
