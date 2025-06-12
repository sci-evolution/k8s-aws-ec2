#!/bin/bash
# Script to run Django tests with coverage and generate reports

# Step 1: Run tests with coverage
coverage run --source='.' webapp/manage.py test tasks

# Step 2: Show coverage report in terminal
coverage report

# Step 3: Generate HTML coverage report in webapp/htmlcov
coverage html -d htmlcov

echo "\nHTML coverage report generated at htmlcov/index.html"
