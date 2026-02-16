@echo off
REM Setup script for SkyHigh Insights - Airline Executive Dashboard (Windows)

echo.
echo SkyHigh Insights - Setup Script
echo ===============================
echo.

REM Check Python version
echo Checking Python version...
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Setup environment variables
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo. >> .env
    echo Generated .env file. Please add your IBM DB2 credentials
) else (
    echo .env file already exists
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env and add your IBM DB2 credentials:
echo    - DB_USERNAME
echo    - DB_PASSWORD
echo    - DB_HOST (default: 52.211.123.34)
echo    - DB_PORT (default: 25010)
echo    - DB_NAME (default: IEMASTER)
echo 2. Run tests: python -m unittest test_db2_connector.py -v
echo 3. Run: streamlit run dashboard.py
echo.
pause
