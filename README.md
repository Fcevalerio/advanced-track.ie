# SkyHigh Insights - Executive Airline Dashboard

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-green.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An interactive web application to analyze and visualize airline operations data, built with **Python**, **Streamlit**, and **Plotly**. This project provides a comprehensive Executive Command Center dashboard for analyzing financial health, operational efficiency, and fleet status.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Dashboard](#-running-the-dashboard)
- [Data Pipeline](#-data-pipeline)
- [Project Structure](#-project-structure)
- [GitHub Actions Workflow](#-github-actions-workflow)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### **Executive Summary**
- Real-time KPIs and high-level metrics
- Key performance indicators at a glance

### **Financial Performance**
- Total revenue tracking
- Revenue analysis by route and ticket class
- Revenue per Available Seat Mile (RASM) calculations
- Ancillary revenue breakdown

### **Fleet Operations**
- Aircraft utilization metrics
- Fuel efficiency leaderboard by aircraft model
- Maintenance alerts and health status
- Load factor analysis (% seats filled)

### **Route Network**
- Geographic visualization of flight routes
- Busiest routes heatmap
- Passenger flow analysis
- Route performance metrics

### **Human Resources**
- Department headcount and budget distribution
- Staffing efficiency ratios
- Salary distribution analysis

### **Technical Highlights**
- ✅ Interactive Visualizations (Plotly)
- ✅ Real-time Data Refresh
- ✅ Responsive Web Interface
- ✅ Fallback Mode (Local Parquet Files)
- ✅ Comprehensive Logging
- ✅ Professional Code Structure

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard                       │
│            (dashboard.py - Interactive UI Layer)             │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────────┐    ┌────────────────────┐
│  DB2 Connector   │    │  Local Connector   │
│(src/connector.py)│    │(Parquet Fallback)  │
└────────┬─────────┘    └────────┬───────────┘
         │                       │
         ▼                       ▼
    ┌────────────────┐   ┌──────────────────┐
    │  IBM DB2 Live  │   │  datasets/ Folder│
    │    Database    │   │ (Parquet Files)  │
    └────────────────┘   └──────────────────┘
```

**Data Flow:**
1. **Extraction**: SQLAlchemy queries from IBM DB2 or reads local Parquet files
2. **Transformation**: Pandas for data manipulation and aggregation
3. **Caching**: Streamlit's `@st.cache_data` for performance
4. **Visualization**: Plotly for interactive charts
5. **Logging**: Dashboard operations logged to `dashboard.log`

---

## 📦 Prerequisites

- **Python 3.10+**
- **IBM DB2 Instance** (optional - dashboard works with local data fallback)
- **pip** or **conda** (package manager)
- **Virtual Environment** (recommended)

### System Requirements
- **OS**: macOS, Linux, or Windows
- **RAM**: 2GB minimum (4GB recommended)
- **Disk**: 500MB for dependencies + datasets

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Fcevalerio/advanced-track.ie.git
cd advanced-track.ie
```

### 2. Create Virtual Environment

**Using venv:**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

**Using conda:**
```bash
conda create -n skyhigh python=3.10
conda activate skyhigh
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `streamlit>=1.28`
- `pandas>=2.0`
- `plotly>=5.17`
- `sqlalchemy>=2.0`
- `python-dotenv>=1.0`
- `ibm_db>=3.1` (optional, for live DB2 connection)

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=your-db2-host.example.com
DB_PORT=50000
DB_NAME=your_database
DB_USERNAME=your_username
DB_PASSWORD=your_password

# Optional: Driver specification (defaults to db2+ibm_db)
DB2_DRIVER=db2+ibm_db

# Dashboard Mode (1 = local fallback, 0 = live DB2)
USE_LOCAL=1
```

**Note:** A `.env.example` file is provided in the repository as a template.

### Running with Local Data (No DB2 Required)

By default, the dashboard runs in **local fallback mode** reading from `datasets/` folder:

```bash
USE_LOCAL=1 streamlit run dashboard.py
```

### Running with Live DB2 Connection

To use the live database (requires DB2 credentials and client):

```bash
USE_LOCAL=0 streamlit run dashboard.py
```

---

## 📊 Running the Dashboard

### Quick Start (Recommended - Local Mode)

```bash
# Activate virtual environment
source venv/bin/activate

# Run dashboard with local data
streamlit run dashboard.py
```

The dashboard will open automatically in your browser at:
- **Local URL**: `http://localhost:8501`
- **Network URL**: `http://<your-ip>:8501`

### With Live Database

```bash
# Set to use live DB2
export USE_LOCAL=0

# Run dashboard
streamlit run dashboard.py
```

### Running in Background (Server Deployment)

```bash
# Start as background process
nohup streamlit run dashboard.py > streamlit.log 2>&1 &

# View logs
tail -f streamlit.log

# Stop the process
pkill -f streamlit
```

---

## 📈 Data Pipeline

### Data Sources

1. **IBM DB2 Database** (Primary)
   - 9 main tables: AIRPLANES, AIRPORTS, COUNTRIES, DEPARTMENT, EMPLOYEE, FLIGHTS, PASSENGERS, ROUTES, TICKETS
   - Real-time data for live analytics
   - Schema: `IEPLANE`

2. **Local Parquet Files** (Fallback)
   - Located in `datasets/` folder
   - Pre-exported from DB2 using `ATT EDA.ipynb`
   - Enables offline dashboard operation

### Export Process

To export data from DB2 to Parquet:

```bash
# 1. Open the notebook
jupyter notebook ATT\ EDA.ipynb

# 2. Run all cells to export tables to datasets/ folder
# Note: Exports first 10,000 rows per table by default
# Modify LIMIT_PER_TABLE variable to change this
```

---

## 📁 Project Structure

```
advanced-track.ie/
├── dashboard.py                 # Main Streamlit application
├── src/
│   └── connector.py            # DB2Connector and DB2Config classes
├── datasets/                   # Local parquet data (fallback mode)
│   ├── airplanes/
│   ├── airports/
│   ├── countries/
│   ├── department/
│   ├── employee/
│   ├── flights/
│   ├── passengers/
│   ├── routes/
│   └── tickets/
├── notebooks/                  # Jupyter notebooks for analysis
│   └── ATT EDA.ipynb          # Data extraction and EDA
├── tests/                      # Unit tests
├── .env.example               # Environment template
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── LICENSE                    # MIT License
├── pyproject.toml             # Project metadata
└── .github/
    └── workflows/
        └── ci.yml             # GitHub Actions CI/CD
```

---

## 🔄 GitHub Actions Workflow

This project includes automated CI/CD via GitHub Actions.

**Workflow File:** `.github/workflows/ci.yml`

**Automated Checks:**
- ✅ Python linting and code quality
- ✅ Unit tests execution
- ✅ Code coverage analysis
- ✅ Security scanning

**Triggered On:**
- Push to `main` and `feature/*` branches
- Pull requests

**To View Workflow Status:**
1. Go to GitHub repository
2. Click "Actions" tab
3. View latest workflow runs

---

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

---

## 🔧 Troubleshooting

### Issue: `DB2 clidriver not found`

**Solution:** Run in local mode:
```bash
USE_LOCAL=1 streamlit run dashboard.py
```

Or install IBM DB2 client:
```bash
pip install ibm_db
```

### Issue: `ModuleNotFoundError: No module named 'connector'`

**Solution:** Ensure you're in the project root and virtual environment is activated:
```bash
cd advanced-track.ie
source venv/bin/activate
```

### Issue: Streamlit not loading data

**Check logs:**
```bash
tail -f dashboard.log
tail -f streamlit.log
```

**Verify datasets exist:**
```bash
ls -la datasets/
```

### Issue: Port 8501 already in use

**Solution:** Run on different port:
```bash
streamlit run dashboard.py --server.port 8502
```

---

## 📚 Documentation

- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [SQLAlchemy Guide](https://docs.sqlalchemy.org/)
- [IBM DB2 Documentation](https://www.ibm.com/docs/db2/)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Open a Pull Request

**Code Standards:**
- PEP 8 compliant
- Type hints for functions
- Docstrings for classes and methods
- Unit tests for new features

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 📧 Support

For issues and questions:
- Open an issue on [GitHub Issues](https://github.com/Fcevalerio/advanced-track.ie/issues)
- Check existing documentation
- Review logs in `dashboard.log` and `streamlit.log`

---

## 🎯 Roadmap

- [ ] Add user authentication
- [ ] Implement data refresh scheduling
- [ ] Add export functionality (PDF reports)
- [ ] Mobile-responsive design
- [ ] Real-time alerts and notifications

---

**Last Updated:** February 2026  
**Status:** Active Development  
**Project:** IE MBDS Advanced Tech Track
