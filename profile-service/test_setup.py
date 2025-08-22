#!/usr/bin/env python
"""
Simple test script to verify profile service setup
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'profile_service.settings')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

def test_database_connection():
    """Test database connection"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_models():
    """Test if models can be imported"""
    try:
        from profiles.models import Profile, UserInterest, ProfilePicture
        from interests.models import Interest
        print("✅ Models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False

def test_settings():
    """Test Django settings"""
    try:
        print(f"✅ Django version: {django.get_version()}")
        print(f"✅ Database: {settings.DATABASES['default']['ENGINE']}")
        print(f"✅ Installed apps: {len(settings.INSTALLED_APPS)}")
        print(f"✅ Media root: {settings.MEDIA_ROOT}")
        return True
    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Profile Service Setup...\n")
    
    tests = [
        ("Settings", test_settings),
        ("Database Connection", test_database_connection),
        ("Models", test_models),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Profile service is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the setup.")
        return 1

if __name__ == '__main__':
    exit(main())
