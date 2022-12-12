#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

if __name__ == "__main__":
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'TestQuiz/settings_local.py')):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestQuiz.settings_local')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestQuiz.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
