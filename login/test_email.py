#!/usr/bin/env python3
"""
Test script for the email verification system.
Run this after starting your Django server to test if emails are being sent.
"""

import requests
import json

# Base URL - change this if your server runs on a different port
BASE_URL = "http://localhost:8000"

# Test email address
TEST_EMAIL = "charanvenkatareddy678@gmail.com"

def test_request_verification():
    """Test requesting a verification code"""
    url = f"{BASE_URL}/api/users/request-verification/"
    
    # Test data
    data = {
        "email": TEST_EMAIL
    }
    
    print("Testing email verification request...")
    print(f"URL: {url}")
    print(f"Email: {TEST_EMAIL}")
    print(f"Data: {data}")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Verification code request successful!")
            print(f"Check your email ({TEST_EMAIL}) for the verification code.")
            print("The code will expire in 10 minutes.")
        else:
            print("❌ Verification code request failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure your Django server is running.")
        print("Run: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_verify_email():
    """Test verifying an email with a code"""
    url = f"{BASE_URL}/api/users/verify-email/"
    
    # You'll need to get the actual code from your email
    data = {
        "email": TEST_EMAIL,
        "code": "123456"  # Replace with the actual code from your email
    }
    
    print("\nTesting email verification...")
    print(f"URL: {url}")
    print(f"Email: {TEST_EMAIL}")
    print(f"Data: {data}")
    print("⚠️  Make sure to replace '123456' with the actual code from your email!")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Email verification successful!")
        else:
            print("❌ Email verification failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure your Django server is running.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Email Verification System Test")
    print("=" * 60)
    print(f"Testing with email: {TEST_EMAIL}")
    print("=" * 60)
    
    # Test requesting verification code
    test_request_verification()
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("1. Check your email for the verification code")
    print("2. Copy the 6-digit code from the email")
    print("3. Edit this script and replace '123456' with your actual code")
    print("4. Uncomment the line below and run the script again")
    print("5. Or test manually using the verify-email endpoint")
    print("=" * 60)
    
    # Test verifying email (uncomment after you get a code)
    # test_verify_email()
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
