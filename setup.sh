#!/bin/bash
# Setup script for SkyHigh Insights - Airline Executive Dashboard

echo "🚀 SkyHigh Insights - Setup Script"
echo "==================================="

# Check Python version
echo "Checking Python version..."
python --version

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Setup environment variables
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please add your DB credentials"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your IBM DB2 credentials"
echo "   - DB_USERNAME"
echo "   - DB_PASSWORD"
echo "   - DB_HOST (default: 52.211.123.34)"
echo "   - DB_PORT (default: 25010)"
echo "   - DB_NAME (default: IEMASTER)"
echo "2. Run tests: python -m unittest test_db2_connector.py -v"
echo "3. Run: streamlit run dashboard.py"
echo ""
