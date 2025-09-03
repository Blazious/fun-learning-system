#!/usr/bin/env python3
"""
Quick Start Script - One command to get everything running!
Just run: python quick_start.py
"""

import os
import sys
import subprocess
from pathlib import Path

def quick_setup():
    """Quick setup function."""
    print("🚀 Quick Setup for Fun Learning Platform")
    print("=" * 50)
    
    # Check if backend directory exists
    if not Path("backend").exists():
        print("❌ Please run this from the project root directory")
        return
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("backend/venv")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "backend/venv"], check=True)
    
    # Determine pip and python paths
    if os.name == 'nt':  # Windows
        pip_cmd = "backend\\venv\\Scripts\\pip"
        python_cmd = "backend\\venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        pip_cmd = "backend/venv/bin/pip"
        python_cmd = "backend/venv/bin/python"
    
    # Install requirements
    print("📥 Installing dependencies...")
    subprocess.run([pip_cmd, "install", "-r", "backend/requirements.txt"], check=True)
    
    # Create .env if it doesn't exist
    env_file = Path("backend/.env")
    if not env_file.exists():
        print("⚙️  Creating .env file...")
        subprocess.run(["copy", "backend\\env.example", "backend\\.env"] if os.name == 'nt' else ["cp", "backend/env.example", "backend/.env"])
        print("⚠️  Please edit backend/.env with your database credentials")
        input("Press Enter after editing...")
    
    # Run Django commands
    print("📦 Setting up database...")
    subprocess.run([python_cmd, "manage.py", "makemigrations"], cwd="backend", check=True)
    subprocess.run([python_cmd, "manage.py", "migrate"], cwd="backend", check=True)
    
    # Create sample data
    print("🎯 Creating sample data...")
    subprocess.run([python_cmd, "setup_db.py"], cwd="backend", check=True)
    
    # Start server
    print("\n🚀 Starting server...")
    print("🌐 Access at: http://localhost:8000/admin/")
    print("Login: admin@funlearning.com / admin123")
    print("Press Ctrl+C to stop\n")
    
    subprocess.run([python_cmd, "manage.py", "runserver"], cwd="backend")

if __name__ == "__main__":
    try:
        quick_setup()
    except KeyboardInterrupt:
        print("\n👋 Setup stopped by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("Please check your setup and try again")
