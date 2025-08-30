#!/usr/bin/env python3
"""
Phase 1 Integration Test Script
Tests all services are running and accessible with health checks
"""

import requests
import time
import json
from datetime import datetime

# Service URLs and their health check endpoints
SERVICES = {
    'login': {'url': 'http://localhost:8000', 'health_path': '/api/users/health/'},
    'profile': {'url': 'http://localhost:8001', 'health_path': '/api/health/'},
    'posts': {'url': 'http://localhost:8002', 'health_path': '/api/health/'},
    'likes': {'url': 'http://localhost:8003', 'health_path': '/api/health/'},
    'comments': {'url': 'http://localhost:8004', 'health_path': '/api/health/'}
}

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n--- {title} ---")

def test_service_health(service_name, service_info):
    """Test health check endpoint for a service"""
    try:
        health_url = service_info['url'] + service_info['health_path']
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {service_name}: HEALTHY")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Version: {data.get('version', 'unknown')}")
            print(f"   Port: {data.get('port', 'unknown')}")
            print(f"   Timestamp: {data.get('timestamp', 'unknown')}")
            return True
        else:
            print(f"❌ {service_name}: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {service_name}: CONNECTION FAILED (Service not running)")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ {service_name}: TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {service_name}: ERROR - {str(e)}")
        return False

def test_service_discovery():
    """Test that services can discover each other"""
    print_section("Service Discovery Test")
    
    # Test each service's config
    for service_name, service_info in SERVICES.items():
        try:
            # Try to access a basic endpoint to see if service is responsive
            response = requests.get(service_info['url'], timeout=5)
            print(f"✅ {service_name}: Accessible at {service_info['url']}")
        except:
            print(f"❌ {service_name}: Not accessible at {service_info['url']}")

def test_basic_api_endpoints():
    """Test basic API endpoints for each service"""
    print_section("Basic API Endpoints Test")
    
    # Test posts service
    try:
        response = requests.get(f"{SERVICES['posts']['url']}/api/posts/", timeout=5)
        if response.status_code == 200:
            print("✅ Posts Service: /api/posts/ endpoint working")
        else:
            print(f"❌ Posts Service: /api/posts/ returned {response.status_code}")
    except Exception as e:
        print(f"❌ Posts Service: /api/posts/ failed - {str(e)}")
    
    # Test comments service
    try:
        response = requests.get(f"{SERVICES['comments']['url']}/api/users/", timeout=5)
        if response.status_code == 200:
            print("✅ Comments Service: /api/users/ endpoint working")
        else:
            print(f"❌ Comments Service: /api/users/ returned {response.status_code}")
    except Exception as e:
        print(f"❌ Comments Service: /api/users/ failed - {str(e)}")
    
    # Test likes service
    try:
        response = requests.get(f"{SERVICES['likes']['url']}/api/users/", timeout=5)
        if response.status_code == 200:
            print("✅ Likes Service: /api/users/ endpoint working")
        else:
            print(f"❌ Likes Service: /api/users/ returned {response.status_code}")
    except Exception as e:
        print(f"❌ Likes Service: /api/users/ failed - {str(e)}")
    
    # Test profile service
    try:
        response = requests.get(f"{SERVICES['profile']['url']}/api/interests/", timeout=5)
        if response.status_code == 200:
            print("✅ Profile Service: /api/interests/ endpoint working")
        else:
            print(f"❌ Profile Service: /api/interests/ returned {response.status_code}")
    except Exception as e:
        print(f"❌ Profile Service: /api/interests/ failed - {str(e)}")
    
    # Test login service
    try:
        response = requests.get(f"{SERVICES['login']['url']}/api/users/", timeout=5)
        if response.status_code == 200:
            print("✅ Login Service: /api/users/ endpoint working")
        else:
            print(f"❌ Login Service: /api/users/ returned {response.status_code}")
    except Exception as e:
        print(f"❌ Login Service: /api/users/ failed - {str(e)}")

def generate_test_report():
    """Generate a test report summary"""
    print_section("Test Report Summary")
    
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total services tested: {len(SERVICES)}")
    
    # Check if all services are running
    all_healthy = True
    for service_name, service_info in SERVICES.items():
        try:
            health_url = service_info['url'] + service_info['health_path']
            response = requests.get(health_url, timeout=5)
            if response.status_code != 200:
                all_healthy = False
        except:
            all_healthy = False
    
    if all_healthy:
        print("🎉 ALL SERVICES ARE RUNNING AND HEALTHY!")
        print("✅ Phase 1 Integration: SUCCESS")
    else:
        print("⚠️  SOME SERVICES ARE NOT HEALTHY")
        print("❌ Phase 1 Integration: NEEDS ATTENTION")
    
    print("\nNext Steps:")
    print("1. Ensure all services are running with: docker-compose up")
    print("2. Check individual service logs for any errors")
    print("3. Verify port allocations are correct")
    print("4. Test inter-service communication")

def main():
    """Main test function"""
    print_header("PHASE 1 INTEGRATION TEST")
    print("Testing Service Discovery and Health Checks")
    
    print_section("Health Check Tests")
    
    # Test each service's health
    healthy_services = 0
    for service_name, service_info in SERVICES.items():
        if test_service_health(service_name, service_info):
            healthy_services += 1
        time.sleep(1)  # Small delay between requests
    
    print(f"\nHealth Check Summary: {healthy_services}/{len(SERVICES)} services healthy")
    
    # Test service discovery
    test_service_discovery()
    
    # Test basic API endpoints
    test_basic_api_endpoints()
    
    # Generate report
    generate_test_report()

if __name__ == "__main__":
    main()
