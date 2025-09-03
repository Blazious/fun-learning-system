#!/usr/bin/env python3
"""
Simple database setup script for Fun Learning Platform
This script will help you set up the database and environment file.
"""

import os
import subprocess
import sys
from pathlib import Path

def create_env_file():
    """Create .env file from template."""
    env_example = Path("env.example")
    env_file = Path(".env")
    
    if not env_file.exists():
        if env_example.exists():
            # Copy the example file
            with open(env_example, 'r') as src:
                content = src.read()
            
            with open(env_file, 'w') as dst:
                dst.write(content)
            
            print("✅ Created .env file from template")
            print("\n⚠️  IMPORTANT: You need to edit the .env file with your database credentials!")
            print("   Please update these values in backend/.env:")
            print("   - DB_PASSWORD=your_actual_postgres_password")
            print("   - DB_USER=your_postgres_username (usually 'postgres')")
            print("   - DB_NAME=funlearning_db")
            print("   - DB_HOST=localhost")
            print("   - DB_PORT=5432")
            
            input("\nPress Enter after you've updated the .env file...")
            return True
        else:
            print("❌ env.example not found")
            return False
    else:
        print("✅ .env file already exists")
        return True

def check_postgresql_connection():
    """Check if we can connect to PostgreSQL."""
    try:
        import psycopg2
        print("✅ psycopg2 is available")
        
        # Try to connect with current .env settings
        from funlearning.settings import DATABASES
        db_config = DATABASES['default']
        
        print(f"🔍 Testing connection to: {db_config['NAME']} on {db_config['HOST']}:{db_config['PORT']}")
        
        conn = psycopg2.connect(
            dbname=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            port=db_config['PORT']
        )
        conn.close()
        print("✅ Database connection successful!")
        return True
        
    except ImportError:
        print("❌ psycopg2 not installed. Please run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 To fix this:")
        print("1. Make sure PostgreSQL is running")
        print("2. Create the database: createdb funlearning_db")
        print("3. Check your .env file has correct credentials")
        print("4. Make sure the postgres user has the right password")
        return False

def create_database():
    """Try to create the database if it doesn't exist."""
    print("\n🔧 Attempting to create database...")
    
    try:
        # Try to create the database using createdb command
        result = subprocess.run(['createdb', '-U', 'postgres', 'funlearning_db'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database 'funlearning_db' created successfully")
            return True
        else:
            print(f"⚠️  Could not create database: {result.stderr}")
            print("   You may need to create it manually:")
            print("   - Connect to PostgreSQL: psql -U postgres")
            print("   - Create database: CREATE DATABASE funlearning_db;")
            print("   - Exit: \\q")
            return False
            
    except FileNotFoundError:
        print("⚠️  'createdb' command not found")
        print("   Please create the database manually:")
        print("   - Connect to PostgreSQL: psql -U postgres")
        print("   - Create database: CREATE DATABASE funlearning_db;")
        print("   - Exit: \\q")
        return False

def main():
    """Main setup function."""
    print("🚀 Fun Learning Platform - Database Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Please run this script from the backend directory")
        return
    
    # Step 1: Create .env file
    print("\n📝 Step 1: Setting up environment file...")
    if not create_env_file():
        return
    
    # Step 2: Try to create database
    print("\n🗄️  Step 2: Setting up database...")
    create_database()
    
    # Step 3: Test connection
    print("\n🔍 Step 3: Testing database connection...")
    if check_postgresql_connection():
        print("\n🎉 Database setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run migrations: python manage.py migrate")
        print("2. Create sample data: python setup_db.py")
        print("3. Start server: python manage.py runserver")
    else:
        print("\n❌ Database setup failed. Please fix the issues above and try again.")

if __name__ == "__main__":
    main()
