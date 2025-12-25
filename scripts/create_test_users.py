#!/usr/bin/env python
"""
Script to create test users for login testing
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

def create_test_users():
    print("=" * 50)
    print("CREATING TEST USERS")
    print("=" * 50)

    # Create admin user
    try:
        admin = UserService.get_user_by_email('admin@travel.com')
        if not admin:
            admin = UserService.create_user(
                full_name='Admin User',
                email='admin@travel.com',
                phone='0123456789',
                password='admin123',
                address='Admin Office',
                role='admin'
            )
            print(f"\n✓ Created admin user: admin@travel.com / admin123")
        else:
            print(f"✓ Admin user already exists: admin@travel.com")
    except Exception as e:
        print(f"\n✗ Error creating admin: {e}")

    # Create additional admin user
    try:
        admin11 = UserService.get_user_by_email('admin11@travel.com')
        if not admin11:
            admin11 = UserService.create_user(
                full_name='admin11',
                email='admin11@travel.com',
                phone='0123456789',
                password='admin123',
                address='Admin Office',
                role='admin'
            )
            print(f"✓ Created additional admin user: admin11@travel.com / admin123")
        else:
            print(f"✓ Additional admin user already exists: admin11@travel.com")
    except Exception as e:
        print(f"✗ Error creating additional admin: {e}")

    # Create regular user
    try:
        user = UserService.get_user_by_email('user@travel.com')
        if not user:
            user = UserService.create_user(
                full_name='Test User',
                email='user@travel.com',
                phone='0987654321',
                password='user123',
                address='User Address',
                role='user'
            )
            print(f"✓ Created regular user: user@travel.com / user123")
        else:
            print(f"✓ Regular user already exists: user@travel.com")
    except Exception as e:
        print(f"✗ Error creating user: {e}")

    print("\n" + "=" * 50)
    print("TEST CREDENTIALS:")
    print("  Admin: admin@travel.com / admin123")
    print("  Admin11: admin11@travel.com / admin123")
    print("  User:  user@travel.com / user123")
    print("=" * 50)


if __name__ == '__main__':
    create_test_users()