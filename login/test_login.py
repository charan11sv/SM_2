#!/usr/bin/env python3
"""
Test script for the login functionality
This script demonstrates how to use the login API endpoints
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000/users"

def test_login_flow():
    """Test the complete login flow"""
    
    print("=== Testing Login Flow ===\n")
    
    # Test data
    test_user = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "testpassword123"
    }
    
    # Step 1: Request verification code
    print("1. Requesting verification code...")
    response = requests.post(f"{BASE_URL}/request-verification/", json={"email": test_user["email"]})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    if response.status_code != 200:
        print("Failed to request verification code")
        return
    
    # Step 2: Verify email (you'll need to check your email for the code)
    print("2. Please check your email for the verification code and enter it below:")
    verification_code = input("Enter verification code: ").strip()
    
    print("\nVerifying email...")
    response = requests.post(f"{BASE_URL}/verify-email/", json={
        "email": test_user["email"],
        "code": verification_code
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    if response.status_code != 200:
        print("Failed to verify email")
        return
    
    # Step 3: Onboard user
    print("3. Onboarding user...")
    response = requests.post(f"{BASE_URL}/onboard/", json={
        "first_name": test_user["first_name"],
        "last_name": test_user["last_name"],
        "email": test_user["email"],
        "password": test_user["password"],
        "verification_code": verification_code
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    if response.status_code != 201:
        print("Failed to onboard user")
        return
    
    # Step 4: Login
    print("4. Logging in...")
    response = requests.post(f"{BASE_URL}/login/", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    if response.status_code != 200:
        print("Failed to login")
        return
    
    # Extract tokens
    login_data = response.json()
    access_token = login_data["tokens"]["access"]
    refresh_token = login_data["tokens"]["refresh"]
    
    # Step 5: Get user profile (requires authentication)
    print("5. Getting user profile...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    # Step 6: Test token refresh
    print("6. Testing token refresh...")
    response = requests.post(f"{BASE_URL}/token/refresh/", json={
        "refresh": refresh_token
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    if response.status_code == 200:
        # Update tokens with new ones
        new_tokens = response.json()["tokens"]
        access_token = new_tokens["access"]
        refresh_token = new_tokens["refresh"]
        print("Tokens refreshed successfully!")
        print(f"New access token: {access_token[:50]}...")
        print(f"New refresh token: {refresh_token[:50]}...\n")
    
    # Step 7: Test profile access with new token
    print("7. Testing profile access with refreshed token...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    # Step 8: Logout
    print("8. Logging out...")
    response = requests.post(f"{BASE_URL}/logout/", json={
        "refresh_token": refresh_token
    }, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    print("=== Login Flow Test Complete ===")

def test_existing_user_login():
    """Test login with existing user credentials"""
    
    print("\n=== Testing Existing User Login ===\n")
    
    # Test login with the user we just created
    test_credentials = {
        "email": "john.doe@example.com",
        "password": "testpassword123"
    }
    
    print("Attempting to login with existing user...")
    response = requests.post(f"{BASE_URL}/login/", json=test_credentials)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    if response.status_code == 200:
        print("Login successful!")
        
        # Test token refresh
        login_data = response.json()
        refresh_token = login_data["tokens"]["refresh"]
        
        print("Testing token refresh...")
        response = requests.post(f"{BASE_URL}/token/refresh/", json={
            "refresh": refresh_token
        })
        print(f"Token refresh status: {response.status_code}")
        print(f"Token refresh response: {response.json()}\n")
    else:
        print("Login failed!")

if __name__ == "__main__":
    print("Login API Test Script")
    print("Make sure your Django server is running on localhost:8000")
    print("=" * 50)
    
    try:
        test_login_flow()
        test_existing_user_login()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Test failed with error: {e}")
