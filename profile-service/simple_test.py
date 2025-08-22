#!/usr/bin/env python3
"""
Simple test to isolate profile setup issue
"""

import requests
import json

def simple_test():
    """Simple test of profile setup"""
    
    # Step 1: Get JWT token
    print("🔑 Getting JWT token...")
    login_data = {
        "email": "charansv.fl678@gmail.com",
        "password": "charansv.fl"
    }
    
    try:
        response = requests.post("http://host.docker.internal:8000/api/users/login/", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['tokens']['access']
            print(f"✅ Token received")
            
            # Step 2: Test profile setup with minimal data
            print("\n🚀 Testing profile setup...")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Try with minimal profile data
            profile_data = {
                "username": "testuser",
                "bio": "Test bio",
                "interests": [1]
            }
            
            print(f"Request data: {profile_data}")
            print(f"Headers: {headers}")
            
            response = requests.post("http://localhost:8001/api/profiles/setup/", 
                                  headers=headers, json=profile_data)
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response content: {response.text}")
            
            if response.status_code == 201:
                print("✅ Profile created successfully!")
            else:
                print("❌ Profile creation failed")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_test()
