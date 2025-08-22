#!/usr/bin/env python3
"""
Simple test script to get JWT token and test profile setup
"""

import requests
import json

def test_profile_setup():
    """Test profile setup with JWT token"""
    
    # Step 1: Login to get JWT token
    print("🔑 Step 1: Getting JWT token...")
    login_data = {
        "email": "charansv.fl678@gmail.com",
        "password": "charansv.fl"
    }
    
    try:
        # Use host.docker.internal to reach the host machine from inside Docker
        response = requests.post("http://host.docker.internal:8000/api/users/login/", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['tokens']['access']
            print(f"✅ Login successful! Token received: {access_token[:50]}...")
            
            # Step 2: Test profile status
            print("\n📊 Step 2: Checking profile status...")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get("http://localhost:8001/api/profiles/status/", headers=headers)
            
            if response.status_code == 200:
                status = response.json()
                print(f"✅ Profile status: {status}")
                
                if not status.get('exists', False):
                    # Step 3: Setup profile
                    print("\n🚀 Step 3: Setting up initial profile...")
                    
                    profile_data = {
                        "username": "charanreddy",
                        "bio": "Hi! I'm Charan, excited to be here and explore the platform!",
                        "interests": [1, 2, 3, 4, 5]  # First 5 interests
                    }
                    
                    response = requests.post("http://localhost:8001/api/profiles/setup/", 
                                          headers=headers, json=profile_data)
                    
                    if response.status_code == 201:
                        profile = response.json()
                        print(f"✅ Profile created successfully!")
                        print(f"   👤 Username: {profile.get('username')}")
                        print(f"   📝 Bio: {profile.get('bio')}")
                        print(f"   🎯 Interests: {len(profile.get('interests', []))}")
                        print(f"   🆔 User ID: {profile.get('user_id')}")
                    else:
                        print(f"❌ Profile setup failed: {response.status_code}")
                        print(f"   Error: {response.text}")
                else:
                    print(f"ℹ️  Profile already exists")
                    
            else:
                print(f"❌ Failed to check profile status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_profile_setup()
