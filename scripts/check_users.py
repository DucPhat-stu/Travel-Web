#!/usr/bin/env python
"""
Script to check users in the database
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User

def main():
    print("=" * 50)
    print("CHECKING USERS IN DATABASE")
    print("=" * 50)
    
    total_users = User.objects.count()
    admin_users = User.objects.filter(role='admin').count()
    regular_users = User.objects.filter(role='user').count()
    
    print(f"\nTotal users: {total_users}")
    print(f"Admin users: {admin_users}")
    print(f"Regular users: {regular_users}")
    
    if total_users > 0:
        print("\nUser list:")
        for user in User.objects.all()[:10]:
            status = "Active" if user.is_active else "Inactive"
            print(f"  - {user.email} | {user.full_name} | Role: {user.role} | Status: {status}")
    else:
        print("\nNo users found in database!")
        print("You need to create users first.")
    
    print("\n" + "=" * 50)

if __name__ == '__main__':
    main()