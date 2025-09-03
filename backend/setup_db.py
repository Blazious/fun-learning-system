#!/usr/bin/env python
"""
Database setup script for Fun Learning Platform
Run this script to initialize the database with sample data
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funlearning.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import connection
from users.models import Profile, Badge, Community
from communities.models import Community as CommunityModel
from learning_sessions.models import Session
from career.models import Skill, CareerPath

User = get_user_model()

def create_superuser():
    """Create a superuser if none exists."""
    if not User.objects.filter(is_superuser=True).exists():
        print("Creating superuser...")
        User.objects.create_superuser(
            email='admin@funlearning.com',
            username='admin',
            password='admin123'
        )
        print("✅ Superuser created: admin@funlearning.com / admin123")
    else:
        print("✅ Superuser already exists")

def create_sample_badges():
    """Create sample badges for the gamification system."""
    badges_data = [
        {
            'name': 'First Session',
            'description': 'Hosted your first learning session',
            'badge_type': 'achievement',
            'required_points': 0,
            'rarity': 'common'
        },
        {
            'name': 'Active Speaker',
            'description': 'Hosted 5 sessions',
            'badge_type': 'milestone',
            'required_points': 250,
            'rarity': 'uncommon'
        },
        {
            'name': 'Community Leader',
            'description': 'Became a community moderator',
            'badge_type': 'achievement',
            'required_points': 100,
            'rarity': 'rare'
        },
        {
            'name': 'Knowledge Sharer',
            'description': 'Published 10 articles',
            'badge_type': 'milestone',
            'required_points': 250,
            'rarity': 'uncommon'
        },
        {
            'name': 'Mentor',
            'description': 'Started mentoring others',
            'badge_type': 'achievement',
            'required_points': 200,
            'rarity': 'rare'
        }
    ]
    
    for badge_data in badges_data:
        Badge.objects.get_or_create(
            name=badge_data['name'],
            defaults=badge_data
        )
    
    print(f"✅ Created {len(badges_data)} sample badges")

def create_sample_skills():
    """Create sample skills for the career system."""
    skills_data = [
        {'name': 'Python', 'category': 'technical', 'subcategory': 'Programming Languages'},
        {'name': 'Django', 'category': 'technical', 'subcategory': 'Web Frameworks'},
        {'name': 'React', 'category': 'technical', 'subcategory': 'Frontend Frameworks'},
        {'name': 'JavaScript', 'category': 'technical', 'subcategory': 'Programming Languages'},
        {'name': 'PostgreSQL', 'category': 'technical', 'subcategory': 'Databases'},
        {'name': 'Docker', 'category': 'technical', 'subcategory': 'DevOps'},
        {'name': 'Git', 'category': 'technical', 'subcategory': 'Version Control'},
        {'name': 'Machine Learning', 'category': 'domain', 'subcategory': 'AI/ML'},
        {'name': 'Data Science', 'category': 'domain', 'subcategory': 'Analytics'},
        {'name': 'Leadership', 'category': 'soft', 'subcategory': 'Management'},
        {'name': 'Communication', 'category': 'soft', 'subcategory': 'Interpersonal'},
        {'name': 'Problem Solving', 'category': 'soft', 'subcategory': 'Critical Thinking'}
    ]
    
    for skill_data in skills_data:
        Skill.objects.get_or_create(
            name=skill_data['name'],
            defaults=skill_data
        )
    
    print(f"✅ Created {len(skills_data)} sample skills")

def create_sample_career_paths():
    """Create sample career paths."""
    career_paths_data = [
        {
            'name': 'Full Stack Developer',
            'description': 'Develop both frontend and backend applications',
            'industry': 'Technology',
            'level': 'mid',
            'required_skills': ['Python', 'JavaScript', 'Django', 'React'],
            'recommended_skills': ['PostgreSQL', 'Docker', 'Git']
        },
        {
            'name': 'Data Scientist',
            'description': 'Analyze data and build machine learning models',
            'industry': 'Technology',
            'level': 'mid',
            'required_skills': ['Python', 'Machine Learning', 'Data Science'],
            'recommended_skills': ['PostgreSQL', 'Git', 'Statistics']
        },
        {
            'name': 'DevOps Engineer',
            'description': 'Manage infrastructure and deployment pipelines',
            'industry': 'Technology',
            'level': 'mid',
            'required_skills': ['Docker', 'Git', 'Linux'],
            'recommended_skills': ['Python', 'PostgreSQL', 'Cloud Platforms']
        }
    ]
    
    for path_data in career_paths_data:
        CareerPath.objects.get_or_create(
            name=path_data['name'],
            defaults=path_data
        )
    
    print(f"✅ Created {len(career_paths_data)} sample career paths")

def create_sample_communities():
    """Create sample communities."""
    communities_data = [
        {
            'name': 'JKUAT Tech Community',
            'description': 'Technology community for JKUAT students and alumni',
            'community_type': 'institution',
            'category': 'Technology',
            'institution': 'Jomo Kenyatta University of Agriculture and Technology',
            'is_public': True
        },
        {
            'name': 'Django Developers Kenya',
            'description': 'Community for Django developers in Kenya',
            'community_type': 'subject',
            'category': 'Web Development',
            'is_public': True
        },
        {
            'name': 'AI/ML Enthusiasts',
            'description': 'Community for artificial intelligence and machine learning enthusiasts',
            'community_type': 'subject',
            'category': 'AI/ML',
            'is_public': True
        },
        {
            'name': 'DevOps Kenya',
            'description': 'DevOps community for professionals in Kenya',
            'community_type': 'subject',
            'category': 'DevOps',
            'is_public': True
        }
    ]
    
    for community_data in communities_data:
        CommunityModel.objects.get_or_create(
            name=community_data['name'],
            defaults=community_data
        )
    
    print(f"✅ Created {len(communities_data)} sample communities")

def create_sample_user():
    """Create a sample user for testing."""
    if not User.objects.filter(email='demo@funlearning.com').exists():
        print("Creating sample user...")
        user = User.objects.create_user(
            email='demo@funlearning.com',
            username='demo_user',
            password='demo123'
        )
        
        # Create profile
        Profile.objects.create(
            user=user,
            bio='Sample user for testing the platform',
            role='listener',
            interests=['Python', 'Web Development', 'Learning'],
            academic={'institution': 'Sample University', 'current_status': 'Student'},
            professional={'company': 'Sample Company', 'role': 'Developer'}
        )
        
        print("✅ Sample user created: demo@funlearning.com / demo123")
    else:
        print("✅ Sample user already exists")

def check_database_connection():
    """Check if database connection is working."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Fun Learning Platform Database...")
    print("=" * 50)
    
    # Check database connection
    if not check_database_connection():
        print("Please check your database configuration and try again.")
        return
    
    # Run migrations first
    print("\n📦 Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return
    
    # Create sample data
    print("\n🎯 Creating sample data...")
    
    create_superuser()
    create_sample_badges()
    create_sample_skills()
    create_sample_career_paths()
    create_sample_communities()
    create_sample_user()
    
    print("\n🎉 Database setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the development server: python manage.py runserver")
    print("2. Access admin panel: http://localhost:8000/admin/")
    print("3. Login with: admin@funlearning.com / admin123")
    print("4. Test sample user: demo@funlearning.com / demo123")

if __name__ == '__main__':
    main()
