#!/usr/bin/env python3
"""
Test complete profile setup with realistic data
"""

import requests
import json

def test_complete_profile_setup():
    """Test complete profile setup with realistic data"""
    
    # Step 1: Get JWT token
    print("🔑 Step 1: Getting JWT token...")
    login_data = {
        "email": "charansv.fl678@gmail.com",
        "password": "charansv.fl"
    }
    
    try:
        response = requests.post("http://host.docker.internal:8000/api/users/login/", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['tokens']['access']
            print(f"✅ Login successful! Token received")
            
            # Step 2: Test profile setup with realistic data
            print("\n🚀 Step 2: Setting up complete profile...")
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Create a realistic profile
            profile_data = {
                "username": "charanreddy",
                "bio": "Hi! I'm Charan, a passionate developer who loves technology, music, and fitness. Always excited to learn new things and connect with like-minded people!",
                "interests": [1, 2, 3, 4, 5]  # Programming, AI, Web Dev, Mobile Apps, Cybersecurity
            }
            
            print(f"📝 Profile Data:")
            print(f"   Username: {profile_data['username']}")
            print(f"   Bio: {profile_data['bio'][:50]}...")
            print(f"   Interests: {len(profile_data['interests'])} selected")
            
            response = requests.post("http://localhost:8001/api/profiles/setup/", 
                                  headers=headers, json=profile_data)
            
            if response.status_code == 201:
                profile = response.json()
                print(f"\n✅ Profile created successfully!")
                print(f"   🆔 Profile ID: {profile.get('id')}")
                print(f"   👤 Username: {profile.get('username')}")
                print(f"   📝 Bio: {profile.get('bio')[:50]}...")
                print(f"   🎯 Interests Count: {profile.get('interests_count')}")
                print(f"   📸 Has Profile Picture: {bool(profile.get('profile_picture'))}")
                print(f"   ✅ Is Complete: {profile.get('is_complete')}")
                
                # Show the interests that were added
                if 'user_interests' in profile:
                    print(f"\n🎯 Interests Added:")
                    for user_interest in profile['user_interests']:
                        interest = user_interest['interest']
                        print(f"   • {interest['name']} ({interest['category_display']})")
                
            else:
                print(f"❌ Profile setup failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_profile_setup()
