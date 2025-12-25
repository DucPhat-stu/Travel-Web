#!/usr/bin/env python
"""
Script to diagnose and fix 400 Bad Request errors
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Load environment before Django setup
from dotenv import load_dotenv
load_dotenv()

django.setup()

from django.conf import settings

def check_settings():
    print("=" * 60)
    print("DJANGO SETTINGS DIAGNOSTIC")
    print("=" * 60)
    
    print("\n1. DEBUG MODE")
    print(f"   DEBUG = {settings.DEBUG}")
    print(f"   Type: {type(settings.DEBUG)}")
    
    print("\n2. ALLOWED_HOSTS")
    print(f"   ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
    print(f"   Type: {type(settings.ALLOWED_HOSTS)}")
    
    print("\n3. SECRET_KEY")
    print(f"   SECRET_KEY exists: {bool(settings.SECRET_KEY)}")
    print(f"   Length: {len(settings.SECRET_KEY)}")
    
    print("\n4. DATABASE")
    print(f"   ENGINE: {settings.DATABASES['default']['ENGINE']}")
    print(f"   NAME: {settings.DATABASES['default']['NAME']}")
    print(f"   HOST: {settings.DATABASES['default']['HOST']}")
    print(f"   PORT: {settings.DATABASES['default']['PORT']}")
    
    print("\n5. MIDDLEWARE")
    for i, middleware in enumerate(settings.MIDDLEWARE, 1):
        print(f"   {i}. {middleware}")
    
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    issues = []
    
    if not settings.DEBUG:
        if '*' in settings.ALLOWED_HOSTS:
            issues.append("⚠️  ALLOWED_HOSTS contains '*' but DEBUG=False")
        if not settings.ALLOWED_HOSTS:
            issues.append("❌ ALLOWED_HOSTS is empty with DEBUG=False")
    
    if len(settings.SECRET_KEY) < 50:
        issues.append("⚠️  SECRET_KEY is too short (should be 50+ characters)")
    
    if 'django.middleware.csrf.CsrfViewMiddleware' not in settings.MIDDLEWARE:
        issues.append("❌ CSRF middleware is missing")
    
    if issues:
        print("\nIssues found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✅ All settings look good!")
    
    print("\n" + "=" * 60)
    print("TESTING ALLOWED_HOSTS")
    print("=" * 60)
    
    test_hosts = ['localhost', '127.0.0.1', 'localhost:8000', '127.0.0.1:8000']
    
    for host in test_hosts:
        if '*' in settings.ALLOWED_HOSTS or host.split(':')[0] in settings.ALLOWED_HOSTS:
            print(f"  ✅ {host} - ALLOWED")
        else:
            print(f"  ❌ {host} - BLOCKED (will cause 400 error)")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    check_settings()