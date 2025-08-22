#!/usr/bin/env python3
"""
Test profile status and verify interests count
"""

import requests
import json

def test_profile_status():
    """Test profile status endpoint"""
    
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
            print(f"✅ Login successful!")
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Step 2: Check profile status
            print("\n📊 Checking profile status...")
            response = requests.get("http://localhost:8001/api/profiles/status/", headers=headers)
            
            if response.status_code == 200:
                status = response.json()
                print(f"✅ Profile Status Response:")
                print(f"   Is complete: {status.get('is_complete')}")
                print(f"   Has username: {status.get('has_username')}")
                print(f"   Has picture: {status.get('has_picture')}")
                print(f"   Interests count: {status.get('interests_count')}")
                print(f"   Missing fields: {status.get('missing_fields')}")
            
            # Step 3: Get full profile
            print("\n👤 Getting full profile...")
            response = requests.get("http://localhost:8001/api/profiles/my_profile/", headers=headers)
            
            if response.status_code == 200:
                profile = response.json()
                print(f"✅ Full Profile Response:")
                print(f"   Username: {profile.get('username')}")
                print(f"   Bio: {profile.get('bio')[:50]}...")
                print(f"   Interests Count: {profile.get('interests_count')}")
                print(f"   Profile Picture: {profile.get('profile_picture_url') or 'None'}")
                
                # Show interests
                if 'user_interests' in profile:
                    print(f"\n🎯 Interests in Response:")
                    for user_interest in profile['user_interests']:
                        interest = user_interest['interest']
                        print(f"   • {interest['name']} ({interest['category_display']})")
                        
            # Step 4: Test a simple GET request to the profile
            print("\n🔍 Testing direct profile GET...")
            response = requests.get("http://localhost:8001/api/profiles/1/", headers=headers)
            
            if response.status_code == 200:
                profile = response.json()
                print(f"✅ Direct Profile GET Response:")
                print(f"   Interests Count: {profile.get('interests_count')}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_profile_status()
