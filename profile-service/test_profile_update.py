#!/usr/bin/env python3
"""
Test profile updates and management features
"""

import requests
import json

def test_profile_management():
    """Test profile management features"""
    
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
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Step 2: Check profile status
            print("\n📊 Step 2: Checking profile status...")
            response = requests.get("http://localhost:8001/api/profiles/status/", headers=headers)
            
            if response.status_code == 200:
                status = response.json()
                print(f"✅ Profile Status:")
                print(f"   Profile exists: True")
                print(f"   Is complete: {status.get('is_complete')}")
                print(f"   Has username: {status.get('has_username')}")
                print(f"   Has picture: {status.get('has_picture')}")
                print(f"   Interests count: {status.get('interests_count')}")
                print(f"   Missing fields: {status.get('missing_fields')}")
            
            # Step 3: Get current profile
            print("\n👤 Step 3: Getting current profile...")
            response = requests.get("http://localhost:8001/api/profiles/my_profile/", headers=headers)
            
            if response.status_code == 200:
                profile = response.json()
                print(f"✅ Current Profile:")
                print(f"   Username: {profile.get('username')}")
                print(f"   Bio: {profile.get('bio')[:50]}...")
                print(f"   Interests Count: {profile.get('interests_count')}")
                print(f"   Profile Picture: {profile.get('profile_picture_url') or 'None'}")
                
                # Show interests
                if 'user_interests' in profile:
                    print(f"\n🎯 Current Interests:")
                    for user_interest in profile['user_interests']:
                        interest = user_interest['interest']
                        print(f"   • {interest['name']} ({interest['category_display']})")
            
            # Step 4: Test username availability check
            print("\n🔍 Step 4: Testing username availability...")
            test_usernames = ["charanreddy", "newuser123", "admin"]
            
            for username in test_usernames:
                response = requests.post("http://localhost:8001/api/profiles/check_username/", 
                                      headers=headers, json={"username": username})
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   Username '{username}': {'✅ Available' if result.get('available') else '❌ Taken'}")
                else:
                    print(f"   Username '{username}': ❌ Check failed")
            
            # Step 5: Test profile update
            print("\n🔄 Step 5: Testing profile update...")
            update_data = {
                "bio": "Updated bio: I'm Charan, a passionate developer who loves technology, music, and fitness. Always excited to learn new things and connect with like-minded people! This is my updated bio.",
                "interests": [1, 2, 3, 6, 7]  # Programming, AI, Web Dev, Basketball, Tennis
            }
            
            response = requests.put("http://localhost:8001/api/profiles/1/", 
                                  headers=headers, json=update_data)
            
            if response.status_code == 200:
                profile = response.json()
                print(f"✅ Profile updated successfully!")
                print(f"   New bio: {profile.get('bio')[:50]}...")
                print(f"   New interests count: {profile.get('interests_count')}")
                
                # Show updated interests
                if 'user_interests' in profile:
                    print(f"\n🎯 Updated Interests:")
                    for user_interest in profile['user_interests']:
                        interest = user_interest['interest']
                        print(f"   • {interest['name']} ({interest['category_display']})")
            else:
                print(f"❌ Profile update failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_profile_management()
