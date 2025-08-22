#!/usr/bin/env python3
"""
Debug script to decode JWT token and see its structure
"""

import requests
import jwt
import json

def debug_jwt_token():
    """Debug JWT token structure"""
    
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
            print(f"✅ Token received: {access_token[:50]}...")
            
            # Step 2: Decode token (without verification to see payload)
            try:
                # Decode without verification to see the payload
                decoded = jwt.decode(access_token, options={"verify_signature": False})
                print(f"\n📋 JWT Token Payload:")
                print(json.dumps(decoded, indent=2))
                
                # Check for user_id field
                user_id = decoded.get('user_id')
                if user_id:
                    print(f"\n✅ Found user_id: {user_id}")
                else:
                    print(f"\n❌ No user_id field found")
                    print(f"Available fields: {list(decoded.keys())}")
                    
            except Exception as e:
                print(f"❌ Error decoding token: {e}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_jwt_token()
