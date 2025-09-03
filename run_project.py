#!/usr/bin/env python3
"""
Fun Learning Platform - Cross-platform Setup Script
This script will set up and run your Django project automatically.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_header():
    """Print the project header."""
    print("\n" + "=" * 50)
    print("    Fun Learning Platform - Setup")
    print("=" * 50 + "\n")

def check_python():
    """Check if Python is available."""
    print("🔍 Checking Python installation...")
    if sys.version_info < (3, 8):
        print(f"❌ Python {sys.version} is too old. Please install Python 3.8+")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} found")
    return True

def check_postgresql():
    """Check if PostgreSQL is accessible."""
    print("🔍 Checking PostgreSQL connection...")
    try:
        import psycopg2
        # Try to connect with default credentials
        conn = psycopg2.connect(
            dbname='funlearning_db',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        conn.close()
        print("✅ Database connection successful")
        return True
    except ImportError:
        print("⚠️  psycopg2 not installed (will be installed with requirements)")
        return False
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("Please ensure PostgreSQL is running and database 'funlearning_db' exists")
        return False

def setup_virtual_environment():
    """Set up Python virtual environment."""
    print("📦 Setting up virtual environment...")
    
    venv_path = Path("backend/venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "backend/venv"], check=True)
            print("✅ Virtual environment created")
        except subprocess.CalledProcessError:
            print("❌ Failed to create virtual environment")
            return False
    else:
        print("✅ Virtual environment already exists")
    
    return True

def get_activate_command():
    """Get the appropriate activate command for the current OS."""
    if platform.system() == "Windows":
        return "backend\\venv\\Scripts\\activate"
    else:
        return "source backend/venv/bin/activate"

def install_requirements():
    """Install Python requirements."""
    print("📥 Installing dependencies...")
    
    # Determine the pip executable
    if platform.system() == "Windows":
        pip_cmd = "backend\\venv\\Scripts\\pip"
    else:
        pip_cmd = "backend/venv/bin/pip"
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "backend/requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_environment_file():
    """Set up the environment configuration file."""
    print("⚙️  Setting up environment configuration...")
    
    env_example = Path("backend/env.example")
    env_file = Path("backend/.env")
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print("✅ Environment file created from template")
            print("⚠️  Please edit backend/.env with your database credentials")
            
            # Give user a chance to edit the file
            input("Press Enter after editing the .env file...")
        else:
            print("❌ env.example not found")
            return False
    else:
        print("✅ Environment file already exists")
    
    return True

def run_django_commands():
    """Run Django management commands."""
    print("📦 Running Django setup commands...")
    
    # Determine the python executable
    if platform.system() == "Windows":
        python_cmd = "backend\\venv\\Scripts\\python"
    else:
        python_cmd = "backend/venv/bin/python"
    
    commands = [
        ["makemigrations"],
        ["migrate"],
        ["setup_db.py"]  # This will be run as a script
    ]
    
    for cmd in commands:
        if cmd[0] == "setup_db.py":
            print("🎯 Creating sample data...")
            try:
                # Change to backend directory and run setup script
                os.chdir("backend")
                subprocess.run([python_cmd, "setup_db.py"], check=True)
                os.chdir("..")
            except subprocess.CalledProcessError:
                print("❌ Failed to create sample data")
                return False
        else:
            print(f"Running: python manage.py {cmd[0]}")
            try:
                subprocess.run([python_cmd, "manage.py"] + cmd, cwd="backend", check=True)
            except subprocess.CalledProcessError:
                print(f"❌ Failed to run: python manage.py {cmd[0]}")
                return False
    
    print("✅ Django setup completed")
    return True

def start_server():
    """Start the Django development server."""
    print("\n🚀 Starting development server...")
    print("\n🌐 Access your platform at:")
    print("   - Admin Panel: http://localhost:8000/admin/")
    print("   - API Root: http://localhost:8000/api/")
    print("   - Login: admin@funlearning.com / admin123")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Determine the python executable
    if platform.system() == "Windows":
        python_cmd = "backend\\venv\\Scripts\\python"
    else:
        python_cmd = "backend/venv/bin/python"
    
    try:
        subprocess.run([python_cmd, "manage.py", "runserver"], cwd="backend")
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")

def main():
    """Main setup function."""
    print_header()
    
    # Check if we're in the right directory
    if not Path("backend").exists():
        print("❌ Please run this script from the project root directory")
        print("   (the directory containing the 'backend' folder)")
        return
    
    # Run setup steps
    if not check_python():
        return
    
    if not setup_virtual_environment():
        return
    
    if not install_requirements():
        return
    
    if not setup_environment_file():
        return
    
    # Check PostgreSQL after installing requirements
    check_postgresql()
    
    if not run_django_commands():
        return
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
