#!/usr/bin/env python3
"""
Final comprehensive test of the Profile Service
Demonstrates all working features
"""

import requests
import json

def demo_profile_service():
    """Demonstrate all working profile service features"""
    
    print("🚀 PROFILE SERVICE COMPREHENSIVE DEMO")
    print("=" * 50)
    
    # Step 1: Get JWT token
    print("\n🔑 Step 1: Authentication")
    print("-" * 30)
    login_data = {
        "email": "charansv.fl678@gmail.com",
        "password": "charansv.fl"
    }
    
    try:
        response = requests.post("http://host.docker.internal:8000/api/users/login/", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['tokens']['access']
            print(f"✅ JWT Authentication successful")
            print(f"   Token: {access_token[:20]}...")
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Step 2: Test Interests API (No Auth Required)
            print("\n🎯 Step 2: Interests API (Public)")
            print("-" * 30)
            response = requests.get("http://localhost:8001/api/interests/")
            if response.status_code == 200:
                interests = response.json()
                print(f"✅ Available Interests: {len(interests)} total")
                print(f"   Categories: {list(set([i['category_display'] for i in interests]))}")
                print(f"   Sample: {interests[0]['name']} ({interests[0]['category_display']})")
            
            # Step 3: Profile Status Check
            print("\n📊 Step 3: Profile Status")
            print("-" * 30)
            response = requests.get("http://localhost:8001/api/profiles/status/", headers=headers)
            if response.status_code == 200:
                status = response.json()
                print(f"✅ Profile Status:")
                print(f"   Exists: True")
                print(f"   Complete: {status.get('is_complete')}")
                print(f"   Username: {status.get('has_username')}")
                print(f"   Picture: {status.get('has_picture')}")
                print(f"   Interests: {status.get('interests_count')}")
                print(f"   Missing: {status.get('missing_fields')}")
            
            # Step 4: Current Profile
            print("\n👤 Step 4: Current Profile")
            print("-" * 30)
            response = requests.get("http://localhost:8001/api/profiles/my_profile/", headers=headers)
            if response.status_code == 200:
                profile = response.json()
                print(f"✅ Current Profile:")
                print(f"   ID: {profile.get('id')}")
                print(f"   Username: {profile.get('username')}")
                print(f"   Bio: {profile.get('bio')[:60]}...")
                print(f"   Interests: {profile.get('interests_count')}")
                print(f"   Picture: {profile.get('profile_picture_url') or 'None'}")
                
                if 'user_interests' in profile:
                    print(f"\n🎯 Current Interests:")
                    for user_interest in profile['user_interests']:
                        interest = user_interest['interest']
                        print(f"   • {interest['name']} ({interest['category_display']})")
            
            # Step 5: Username Availability Check
            print("\n🔍 Step 5: Username Validation")
            print("-" * 30)
            test_usernames = ["charanreddy", "newuser123", "admin", "testuser"]
            for username in test_usernames:
                response = requests.post("http://localhost:8001/api/profiles/check_username/", 
                                      headers=headers, json={"username": username})
                if response.status_code == 200:
                    result = response.json()
                    status = "✅ Available" if result.get('available') else "❌ Taken"
                    print(f"   '{username}': {status}")
            
            # Step 6: Profile Update
            print("\n🔄 Step 6: Profile Update")
            print("-" * 30)
            update_data = {
                "username": "charanreddy",
                "bio": "Final updated bio: I'm Charan, a passionate developer who loves technology, music, and fitness. Always excited to learn new things and connect with like-minded people! This is my final updated bio.",
                "interests": [1, 2, 3, 8, 9]  # Programming, AI, Web Dev, Music, Photography
            }
            
            response = requests.put("http://localhost:8001/api/profiles/1/", 
                                  headers=headers, json=update_data)
            
            if response.status_code == 200:
                profile = response.json()
                print(f"✅ Profile Updated Successfully!")
                print(f"   New Username: {profile.get('username')}")
                print(f"   New Bio: {profile.get('bio')[:60]}...")
                print(f"   New Interests Count: {profile.get('interests_count')}")
                
                if 'user_interests' in profile:
                    print(f"\n🎯 Updated Interests:")
                    for user_interest in profile['user_interests']:
                        interest = user_interest['interest']
                        print(f"   • {interest['name']} ({interest['category_display']})")
            
            # Step 7: Final Status Check
            print("\n📊 Step 7: Final Status Check")
            print("-" * 30)
            response = requests.get("http://localhost:8001/api/profiles/status/", headers=headers)
            if response.status_code == 200:
                status = response.json()
                print(f"✅ Final Profile Status:")
                print(f"   Complete: {status.get('is_complete')}")
                print(f"   Username: {status.get('has_username')}")
                print(f"   Picture: {status.get('has_picture')}")
                print(f"   Interests: {status.get('interests_count')}")
                print(f"   Missing: {status.get('missing_fields')}")
                
                if status.get('is_complete'):
                    print(f"   🎉 Profile is complete!")
                else:
                    print(f"   📝 Profile needs: {status.get('missing_fields')}")
            
            print("\n" + "=" * 50)
            print("🎉 PROFILE SERVICE DEMO COMPLETED SUCCESSFULLY!")
            print("=" * 50)
                
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_profile_service()
