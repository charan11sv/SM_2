#!/usr/bin/env python3
"""
Demo script for Profile Service - Complete Profile Setup Flow
This script demonstrates the complete user journey from login to profile setup
"""

import requests
import json
import time

# Service URLs
LOGIN_SERVICE_URL = "http://localhost:8000/api"
PROFILE_SERVICE_URL = "http://localhost:8001/api"

def demo_login_and_profile_setup():
    """Demonstrate complete login and profile setup flow"""
    print("🚀 Profile Service Demo - Complete User Journey")
    print("=" * 60)
    
    # Step 1: Login to get JWT token
    print("\n1️⃣  Step 1: User Login")
    print("-" * 30)
    
    login_data = {
        "email": "demo@example.com",  # Replace with actual user credentials
        "password": "demo123"         # Replace with actual password
    }
    
    try:
        response = requests.post(f"{LOGIN_SERVICE_URL}/login/", json=login_data)
        print(f"   Login request status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access')
            print(f"   ✅ Login successful!")
            print(f"   🔑 Access token received")
            
            # Step 2: Check profile status
            print("\n2️⃣  Step 2: Check Profile Status")
            print("-" * 30)
            
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{PROFILE_SERVICE_URL}/profiles/status/", headers=headers)
            
            if response.status_code == 200:
                status = response.json()
                profile_exists = status.get('exists', False)
                is_complete = status.get('is_complete', False)
                
                print(f"   Profile exists: {profile_exists}")
                print(f"   Profile complete: {is_complete}")
                
                if not profile_exists:
                    # Step 3: Setup initial profile
                    print("\n3️⃣  Step 3: Initial Profile Setup")
                    print("-" * 30)
                    
                    # Get available interests first
                    interests_response = requests.get(f"{PROFILE_SERVICE_URL}/interests/")
                    if interests_response.status_code == 200:
                        interests = interests_response.json()
                        print(f"   Available interests: {len(interests)} found")
                        
                        # Select some interests for demo
                        selected_interests = [interest['id'] for interest in interests[:3]]
                        print(f"   Selected interests: {selected_interests}")
                        
                        # Setup profile
                        profile_data = {
                            "username": "demouser123",
                            "bio": "This is a demo profile created during testing. I'm excited to explore the platform!",
                            "interests": selected_interests
                        }
                        
                        response = requests.post(f"{PROFILE_SERVICE_URL}/profiles/setup/", 
                                              headers=headers, json=profile_data)
                        
                        if response.status_code == 201:
                            profile = response.json()
                            print(f"   ✅ Profile created successfully!")
                            print(f"   👤 Username: {profile.get('username')}")
                            print(f"   📝 Bio: {profile.get('bio')}")
                            print(f"   🎯 Interests: {len(profile.get('interests', []))} selected")
                        else:
                            print(f"   ❌ Profile setup failed: {response.status_code}")
                            print(f"   Error: {response.text}")
                    else:
                        print(f"   ❌ Failed to get interests: {interests_response.status_code}")
                else:
                    print(f"   ℹ️  Profile already exists, skipping setup")
                    
                    # Step 4: Show existing profile
                    print("\n4️⃣  Step 4: View Existing Profile")
                    print("-" * 30)
                    
                    response = requests.get(f"{PROFILE_SERVICE_URL}/profiles/my_profile/", headers=headers)
                    if response.status_code == 200:
                        profile = response.json()
                        print(f"   👤 Username: {profile.get('username')}")
                        print(f"   📝 Bio: {profile.get('bio')}")
                        print(f"   🎯 Interests: {len(profile.get('interests', []))}")
                        print(f"   📸 Has profile picture: {bool(profile.get('profile_picture'))}")
                    else:
                        print(f"   ❌ Failed to get profile: {response.status_code}")
            
            else:
                print(f"   ❌ Failed to check profile status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            print(f"\n   💡 To test this demo:")
            print(f"      1. Make sure login service is running on port 8000")
            print(f"      2. Create a user account in the login service")
            print(f"      3. Update the credentials in this script")
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection error: Make sure login service is running on port 8000")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")

def demo_with_existing_token(jwt_token):
    """Demo profile setup with existing JWT token"""
    print("🚀 Profile Service Demo - Using Existing JWT Token")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    # Check profile status
    print("\n1️⃣  Checking Profile Status...")
    response = requests.get(f"{PROFILE_SERVICE_URL}/profiles/status/", headers=headers)
    
    if response.status_code == 200:
        status = response.json()
        print(f"   ✅ Profile status retrieved")
        print(f"   Profile exists: {status.get('exists', False)}")
        print(f"   Profile complete: {status.get('is_complete', False)}")
        
        if not status.get('exists', False):
            # Setup profile
            print("\n2️⃣  Setting up initial profile...")
            
            profile_data = {
                "username": "demouser456",
                "bio": "Profile created with existing JWT token. Ready to explore!",
                "interests": [1, 2, 3, 4, 5]  # First 5 interests
            }
            
            response = requests.post(f"{PROFILE_SERVICE_URL}/profiles/setup/", 
                                  headers=headers, json=profile_data)
            
            if response.status_code == 201:
                profile = response.json()
                print(f"   ✅ Profile created successfully!")
                print(f"   👤 Username: {profile.get('username')}")
                print(f"   📝 Bio: {profile.get('bio')}")
                print(f"   🎯 Interests: {len(profile.get('interests', []))}")
            else:
                print(f"   ❌ Profile setup failed: {response.status_code}")
                print(f"   Error: {response.text}")
        else:
            print(f"   ℹ️  Profile already exists")
            
    else:
        print(f"   ❌ Failed to check profile status: {response.status_code}")
        print(f"   Error: {response.text}")

def main():
    """Main demo function"""
    import sys
    
    if len(sys.argv) > 1:
        # Use existing JWT token
        jwt_token = sys.argv[1]
        demo_with_existing_token(jwt_token)
    else:
        # Try to login and setup profile
        demo_login_and_profile_setup()
    
    print("\n" + "=" * 60)
    print("🎯 Demo completed!")
    print("   To test with existing JWT token:")
    print("   python demo_profile_setup.py <your_jwt_token>")

if __name__ == "__main__":
    main()
