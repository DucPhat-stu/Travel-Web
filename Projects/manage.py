#!/usr/bin/env python
import os
import sys

def main():
    """Run administrative tasks."""
    # Thiết lập module settings mặc định
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    # In ra log để kiểm tra biến môi trường
    print(f" Using settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}", file=sys.stderr)
    print(f" DEBUG env: {os.environ.get('DEBUG')}", file=sys.stderr)
    print(f" ALLOWED_HOSTS env: {os.environ.get('ALLOWED_HOSTS')}", file=sys.stderr)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed "
            "and available on your PYTHONPATH environment variable? "
            "Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
