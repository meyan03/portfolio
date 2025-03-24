#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_management.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Check if running the server command
    if len(sys.argv) >= 2 and sys.argv[1] == 'runserver' and len(sys.argv) == 2:
        # No address provided in command, use environment variables
        ip = os.getenv("IP", "0.0.0.0")
        port = os.getenv("PORT", "8000")
        sys.argv.append(f"{ip}:{port}")

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
