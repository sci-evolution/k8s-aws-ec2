#!/bin/bash
# Script to run Django tests with coverage and generate reports

# Set environment variables for Django settings
export WEBAPP_DEBUG=1
export WEBAPP_SECRET_KEY="django-insecure-ml3@$n2r2$e0hsx=q!0i5x88$nwcpj(d0t7rqfi4b9@-@))#(!"
export WEBAPP_ALLOWED_HOSTS="http://localhost:8000"

# Step 1: Run tests with coverage
coverage run --source='.' webapp/manage.py test tasks

# Step 2: Show coverage report in terminal
coverage report

# Step 3: Generate HTML coverage report in webapp/htmlcov
coverage html -d htmlcov

echo "\nHTML coverage report generated at htmlcov/index.html"
