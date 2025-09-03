#!/bin/bash

echo
echo "========================================"
echo "    Fun Learning Platform - Setup"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL connection..."
if ! command -v pg_isready &> /dev/null; then
    echo "⚠️  pg_isready not found, skipping PostgreSQL check"
else
    if ! pg_isready -h localhost -p 5432 &> /dev/null; then
        echo "⚠️  PostgreSQL might not be running"
        echo "Please ensure PostgreSQL is started"
        echo
    fi
fi

# Navigate to backend directory
cd backend || {
    echo "❌ Backend directory not found"
    exit 1
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv || {
        echo "❌ Failed to create virtual environment"
        exit 1
    }
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate || {
    echo "❌ Failed to activate virtual environment"
    exit 1
}

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt || {
    echo "❌ Failed to install requirements"
    exit 1
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating environment file..."
    cp env.example .env
    echo
    echo "⚠️  Please edit .env file with your database credentials"
    echo "Press Enter to continue after editing..."
    read
fi

# Check if database exists
echo "🔍 Checking database..."
python3 -c "
import psycopg2
try:
    psycopg2.connect(dbname='funlearning_db', user='postgres', password='postgres', host='localhost', port='5432')
    print('✅ Database connection successful')
except:
    print('⚠️  Database connection failed')
    print('Please create the database: createdb funlearning_db')
" 2>/dev/null

# Run migrations
echo "📦 Running database migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Create sample data
echo "🎯 Creating sample data..."
python3 setup_db.py

# Start the server
echo
echo "🚀 Starting development server..."
echo
echo "🌐 Access your platform at:"
echo "   - Admin Panel: http://localhost:8000/admin/"
echo "   - API Root: http://localhost:8000/api/"
echo "   - Login: admin@funlearning.com / admin123"
echo
echo "Press Ctrl+C to stop the server"
echo

python3 manage.py runserver
