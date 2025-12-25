#!/usr/bin/env python
"""
Script to setup profile feature with migrations
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.management import call_command

def setup_profile():
    print("=" * 60)
    print("SETTING UP PROFILE FEATURE")
    print("=" * 60)
    
    print("\n1. Creating migrations...")
    try:
        call_command('makemigrations', 'users')
        print("✓ Migrations created successfully")
    except Exception as e:
        print(f"✗ Error creating migrations: {e}")
    
    print("\n2. Running migrations...")
    try:
        call_command('migrate')
        print("✓ Migrations applied successfully")
    except Exception as e:
        print(f"✗ Error running migrations: {e}")
    
    print("\n" + "=" * 60)
    print("PROFILE FEATURE SETUP COMPLETE")
    print("=" * 60)
    
    print("\nNew features available:")
    print("  • Edit Profile: /users/profile/edit/")
    print("  • View Profile: /users/profile/")
    print("  • Create Post: /users/post/create/")
    print("\nYou can now:")
    print("  1. Upload avatar")
    print("  2. Edit bio and personal info")
    print("  3. Share travel photos")
    print("  4. View your photo wall")
    print("=" * 60)

if __name__ == '__main__':
    setup_profile()