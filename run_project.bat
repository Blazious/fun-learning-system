@echo off
echo.
echo ========================================
echo    Fun Learning Platform - Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

:: Check if PostgreSQL is running (basic check)
echo 🔍 Checking PostgreSQL connection...
pg_isready -h localhost -p 5432 >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PostgreSQL might not be running
    echo Please ensure PostgreSQL is started
    echo.
)

:: Navigate to backend directory
cd backend
if errorlevel 1 (
    echo ❌ Backend directory not found
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate

:: Install requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

:: Check if .env file exists
if not exist ".env" (
    echo ⚙️  Creating environment file...
    copy env.example .env
    echo.
    echo ⚠️  Please edit .env file with your database credentials
    echo Press any key to continue after editing...
    pause
)

:: Check if database exists
echo 🔍 Checking database...
python -c "import psycopg2; psycopg2.connect(dbname='funlearning_db', user='postgres', password='postgres', host='localhost', port='5432')" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Database 'funlearning_db' not found or connection failed
    echo Please create the database: createdb funlearning_db
    echo.
)

:: Run migrations
echo 📦 Running database migrations...
python manage.py makemigrations
python manage.py migrate

:: Create sample data
echo 🎯 Creating sample data...
python setup_db.py

:: Start the server
echo.
echo 🚀 Starting development server...
echo.
echo 🌐 Access your platform at:
echo    - Admin Panel: http://localhost:8000/admin/
echo    - API Root: http://localhost:8000/api/
echo    - Login: admin@funlearning.com / admin123
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

pause
