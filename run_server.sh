#!/bin/bash
# Script to run Django development server with Python 3.12

cd "$(dirname "$0")"

# Use Python 3.12 from the system framework
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 manage.py runserver
