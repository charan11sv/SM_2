#!/usr/bin/env python3
"""
Script to check existing users in the database
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onboarding.settings')
django.setup()

from users.models import User, EmailVerification

def check_database():
    print("=== Database Check ===")
    
    # Check Users
    print("\n--- Users ---")
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    
    for user in users:
        print(f"User ID: {user.id}")
        print(f"  Email: {user.email}")
        print(f"  Name: {user.first_name} {user.last_name}")
        print(f"  Active: {user.is_active}")
        print(f"  Staff: {user.is_staff}")
        print(f"  Created: {user.date_joined}")
        print()
    
    # Check Email Verifications
    print("\n--- Email Verifications ---")
    verifications = EmailVerification.objects.all()
    print(f"Total verifications: {verifications.count()}")
    
    for verification in verifications:
        print(f"Email: {verification.email}")
        print(f"  Code: {verification.code}")
        print(f"  Created: {verification.created_at}")
        print(f"  Valid: {verification.is_valid()}")
        print()

if __name__ == "__main__":
    check_database()
