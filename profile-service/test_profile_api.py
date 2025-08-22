#!/usr/bin/env python3
"""
Test script for Profile Service API endpoints
This script demonstrates how to interact with the profile service
"""

import requests
import json

# Profile Service Base URL
BASE_URL = "http://localhost:8001/api"

def test_interests_endpoints():
    """Test interests endpoints (no authentication required)"""
    print("🔍 Testing Interests Endpoints...")
    
    # Get all interests
    response = requests.get(f"{BASE_URL}/interests/")
    print(f"✅ GET /interests/ - Status: {response.status_code}")
    if response.status_code == 200:
        interests = response.json()
        print(f"   Found {len(interests)} interests")
        print(f"   Sample: {interests[0]['name']} ({interests[0]['category_display']})")
    
    # Get interest categories
    response = requests.get(f"{BASE_URL}/interests/categories/")
    print(f"✅ GET /interests/categories/ - Status: {response.status_code}")
    if response.status_code == 200:
        categories = response.json()['categories']
        print(f"   Available categories: {', '.join(list(categories.keys())[:5])}...")
    
    # Search interests
    response = requests.get(f"{BASE_URL}/interests/search/?q=Programming")
    print(f"✅ GET /interests/search/?q=Programming - Status: {response.status_code}")
    if response.status_code == 200:
        results = response.json()
        print(f"   Search results: {results['count']} found")

def test_profile_endpoints_without_auth():
    """Test profile endpoints without authentication (should fail)"""
    print("\n🔒 Testing Profile Endpoints (No Auth - Should Fail)...")
    
    endpoints = [
        "/profiles/status/",
        "/profiles/check_username/",
        "/profiles/setup/",
        "/profiles/upload_picture/"
    ]
    
    for endpoint in endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f"❌ GET {endpoint} - Status: {response.status_code}")
        if response.status_code == 401:
            print(f"   Expected: Authentication required")

def test_profile_setup_with_jwt(jwt_token):
    """Test profile setup with JWT token"""
    print(f"\n🔑 Testing Profile Setup with JWT Token...")
    
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    
    # Check profile status
    response = requests.get(f"{BASE_URL}/profiles/status/", headers=headers)
    print(f"✅ GET /profiles/status/ - Status: {response.status_code}")
    if response.status_code == 200:
        status = response.json()
        print(f"   Profile exists: {status.get('exists', False)}")
        print(f"   Is complete: {status.get('is_complete', False)}")
    
    # Check username availability
    data = {"username": "testuser123"}
    response = requests.post(f"{BASE_URL}/profiles/check_username/", 
                           headers=headers, json=data)
    print(f"✅ POST /profiles/check_username/ - Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Username available: {result.get('available', False)}")
    
    # Setup initial profile
    profile_data = {
        "username": "testuser123",
        "bio": "This is a test profile bio for testing purposes.",
        "interests": [1, 2, 3]  # Programming, AI, Web Development
    }
    
    response = requests.post(f"{BASE_URL}/profiles/setup/", 
                           headers=headers, json=profile_data)
    print(f"✅ POST /profiles/setup/ - Status: {response.status_code}")
    if response.status_code == 201:
        profile = response.json()
        print(f"   Profile created successfully!")
        print(f"   User ID: {profile.get('user_id')}")
        print(f"   Username: {profile.get('username')}")
    elif response.status_code == 400:
        error = response.json()
        print(f"   Error: {error}")

def main():
    """Main test function"""
    print("🚀 Profile Service API Test Suite")
    print("=" * 50)
    
    # Test interests endpoints (no auth required)
    test_interests_endpoints()
    
    # Test profile endpoints without auth (should fail)
    test_profile_endpoints_without_auth()
    
    # Test with JWT token if provided
    print("\n" + "=" * 50)
    print("🔑 To test profile setup, you need a JWT token from the login service.")
    print("   You can get one by logging in through:")
    print("   POST http://localhost:8000/api/login/")
    print("\n   Then run this script with:")
    print("   python test_profile_api.py <your_jwt_token>")
    
    # If JWT token provided as command line argument
    import sys
    if len(sys.argv) > 1:
        jwt_token = sys.argv[1]
        test_profile_setup_with_jwt(jwt_token)

if __name__ == "__main__":
    main()
