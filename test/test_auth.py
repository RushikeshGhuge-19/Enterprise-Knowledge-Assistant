#!/usr/bin/env python3
"""
Test script for Week 1 authentication endpoints.

Run this after starting the server:
    python test_auth.py
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def print_test(name: str):
    print(f"\n{YELLOW}Testing: {name}{RESET}")


def print_pass(message: str):
    print(f"{GREEN}✓ {message}{RESET}")


def print_fail(message: str):
    print(f"{RED}✗ {message}{RESET}")


def test_health_check():
    """Test GET /health endpoint."""
    print_test("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_pass(f"Status: {response.status_code}")
            print(f"  Response: {response.json()}")
            return True
        else:
            print_fail(f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Connection error: {e}")
        return False


def test_signup(email: str, password: str):
    """Test POST /auth/signup endpoint."""
    print_test(f"Signup ({email})")
    try:
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print_pass(f"Status: {response.status_code}")
            print(f"  User ID: {data['user_id']}")
            print(f"  Token Type: {data['token_type']}")
            print(f"  Token (first 50 chars): {data['access_token'][:50]}...")
            return True, data
        else:
            print_fail(f"Status: {response.status_code}")
            print(f"  Response: {response.json()}")
            return False, None
    except Exception as e:
        print_fail(f"Error: {e}")
        return False, None


def test_signup_duplicate(email: str):
    """Test POST /auth/signup with duplicate email."""
    print_test(f"Signup Duplicate Email ({email})")
    try:
        payload = {
            "email": email,
            "password": "some_password_123"
        }
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=payload
        )
        
        if response.status_code == 400:
            print_pass(f"Correctly rejected duplicate: {response.json()['detail']}")
            return True
        else:
            print_fail(f"Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Error: {e}")
        return False


def test_login(email: str, password: str):
    """Test POST /auth/login endpoint."""
    print_test(f"Login ({email})")
    try:
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print_pass(f"Status: {response.status_code}")
            print(f"  User ID: {data['user_id']}")
            print(f"  Token Type: {data['token_type']}")
            return True, data
        else:
            print_fail(f"Status: {response.status_code}")
            print(f"  Response: {response.json()}")
            return False, None
    except Exception as e:
        print_fail(f"Error: {e}")
        return False, None


def test_login_invalid_password(email: str):
    """Test POST /auth/login with wrong password."""
    print_test(f"Login Invalid Password ({email})")
    try:
        payload = {
            "email": email,
            "password": "wrong_password_123"
        }
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=payload
        )
        
        if response.status_code == 401:
            print_pass(f"Correctly rejected: {response.json()['detail']}")
            return True
        else:
            print_fail(f"Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Error: {e}")
        return False


def test_get_me(token: str):
    """Test GET /auth/me endpoint (protected)."""
    print_test("Get Current User (Protected)")
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print_pass(f"Status: {response.status_code}")
            print(f"  ID: {data['id']}")
            print(f"  Email: {data['email']}")
            print(f"  Role: {data['role']}")
            print(f"  Created: {data['created_at']}")
            return True
        else:
            print_fail(f"Status: {response.status_code}")
            print(f"  Response: {response.json()}")
            return False
    except Exception as e:
        print_fail(f"Error: {e}")
        return False


def test_get_me_invalid_token():
    """Test GET /auth/me with invalid token."""
    print_test("Get Current User (Invalid Token)")
    try:
        headers = {
            "Authorization": "Bearer invalid_token_xyz"
        }
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=headers
        )
        
        if response.status_code == 401:
            print_pass(f"Correctly rejected: {response.json()['detail']}")
            return True
        else:
            print_fail(f"Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Error: {e}")
        return False


def main():
    """Run all tests."""
    print(f"\n{YELLOW}{'='*60}")
    print("Enterprise Knowledge Assistant - Auth Tests")
    print(f"{'='*60}{RESET}")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Health Check
    tests_total += 1
    if test_health_check():
        tests_passed += 1
    
    # Test 2: Signup
    tests_total += 1
    success, signup_data = test_signup("testuser@example.com", "secure_password_123")
    if success:
        tests_passed += 1
        token = signup_data['access_token']
    else:
        print(f"{RED}Cannot continue without valid token{RESET}")
        return
    
    # Test 3: Signup Duplicate
    tests_total += 1
    if test_signup_duplicate("testuser@example.com"):
        tests_passed += 1
    
    # Test 4: Login
    tests_total += 1
    success, login_data = test_login("testuser@example.com", "secure_password_123")
    if success:
        tests_passed += 1
        token = login_data['access_token']
    
    # Test 5: Login Invalid Password
    tests_total += 1
    if test_login_invalid_password("testuser@example.com"):
        tests_passed += 1
    
    # Test 6: Get Current User
    tests_total += 1
    if test_get_me(token):
        tests_passed += 1
    
    # Test 7: Get Current User Invalid Token
    tests_total += 1
    if test_get_me_invalid_token():
        tests_passed += 1
    
    # Summary
    print(f"\n{YELLOW}{'='*60}")
    print(f"Results: {tests_passed}/{tests_total} tests passed")
    print(f"{'='*60}{RESET}\n")
    
    if tests_passed == tests_total:
        print(f"{GREEN}✓ All tests passed! Week 1 is complete.{RESET}\n")
        return 0
    else:
        print(f"{RED}✗ Some tests failed. Check errors above.{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
