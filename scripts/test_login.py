#!/usr/bin/env python
"""
Script to test login functionality
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User
from users.services import UserService

def test_login():
    print("=" * 60)
    print("TESTING LOGIN FUNCTIONALITY")
    print("=" * 60)
    
    # Test credentials
    test_cases = [
        ('admin@travel.com', 'admin123', 'admin'),
        ('user@travel.com', 'user123', 'user'),
        ('admin@example.com', 'admin', 'admin'),  # existing admin
    ]
    
    for email, password, expected_role in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {email}")
        print(f"Password: {password}")
        print(f"Expected role: {expected_role}")
        print('-' * 60)
        
        # Check if user exists
        user = UserService.get_user_by_email(email)
        if user:
            print(f"✓ User found in database")
            print(f"  - Full name: {user.full_name}")
            print(f"  - Email: {user.email}")
            print(f"  - Role: {user.role}")
            print(f"  - Active: {user.is_active}")
            
            # Test authentication
            auth_user = UserService.authenticate_user(email, password)
            if auth_user:
                print(f"✓ Authentication SUCCESSFUL")
                print(f"  - Redirect to: {'admin_panel:dashboard' if auth_user.is_admin() else 'core:home'}")
            else:
                print(f"✗ Authentication FAILED - Wrong password")
        else:
            print(f"✗ User NOT found in database")
    
    print("\n" + "=" * 60)
    print("SUMMARY - Available Test Accounts:")
    print("=" * 60)
    print("\nAdmin accounts:")
    for user in User.objects.filter(role='admin', is_active=True):
        print(f"  Email: {user.email}")
        print(f"  Name: {user.full_name}")
        print(f"  → Redirects to: /admin-panel/")
        print()
    
    print("Regular user accounts:")
    for user in User.objects.filter(role='user', is_active=True):
        print(f"  Email: {user.email}")
        print(f"  Name: {user.full_name}")
        print(f"  → Redirects to: / (home)")
        print()
    
    print("=" * 60)
    print("\nTo test login:")
    print("1. Run: python manage.py runserver")
    print("2. Open: http://localhost:8000/users/login/")
    print("3. Use the credentials above")
    print("=" * 60)

if __name__ == '__main__':
    test_login()