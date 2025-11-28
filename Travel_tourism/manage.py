#!/usr/bin/env python
import os
import sys

def main():
    # Thử cả 2 đường dẫn
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
    
    if not settings_module:
        # Thử tìm settings.py
        if os.path.exists('src/core/settings.py'):
            settings_module = 'src.core.settings'
        elif os.path.exists('core/settings.py'):
            settings_module = 'core.settings'
        else:
            print("❌ Cannot find settings.py!", file=sys.stderr)
            sys.exit(1)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    
    print(f"⚠️ Using settings module: {settings_module}", file=sys.stderr)
    print(f"⚠️ DEBUG env: {os.environ.get('DEBUG')}", file=sys.stderr)
    print(f"⚠️ ALLOWED_HOSTS env: {os.environ.get('ALLOWED_HOSTS')}", file=sys.stderr)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()