#!/usr/bin/env python
"""
Simple script to set up SQLite database for the FunLearning project.
This script will:
1. Create the database file
2. Run all migrations
3. Create a superuser (optional)
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_database():
    """Set up the SQLite database and run migrations."""
    
    # Add the current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funlearning.settings')
    
    # Setup Django
    django.setup()
    
    print("Setting up SQLite database...")
    
    # Run migrations
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Database setup complete!")
    print("You can now run the development server with: python manage.py runserver")
    
    # Ask if user wants to create a superuser
    create_superuser = input("\nWould you like to create a superuser? (y/n): ").lower().strip()
    
    if create_superuser in ['y', 'yes']:
        print("Creating superuser...")
        execute_from_command_line(['manage.py', 'createsuperuser'])
        print("Superuser created successfully!")
    
    print("\nSetup complete! Your SQLite database is ready to use.")

if __name__ == '__main__':
    setup_database()
