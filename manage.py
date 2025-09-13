#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jet.tests.settings")

    try:
        from django.core.management import execute_from_command_line
    except ModuleNotFoundError as e:
        print("Error: Django is not installed or not found in your environment.")
        print("Details:", e)
        print("Try running 'pip install django' to install it.")
        sys.exit(1)

    execute_from_command_line(sys.argv)
