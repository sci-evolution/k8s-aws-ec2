#!/bin/bash
# Script to run all tests with coverage and generate reports

export WEBAPP_DEBUG=1
export WEBAPP_SECRET_KEY="django-insecure-ml3@$n2r2$e0hsx=q!0i5x88$nwcpj(d0t7rqfi4b9@-@))#(!"
export WEBAPP_ALLOWED_HOSTS="http://localhost:8000"

# Add Django project root to PYTHONPATH for all apps
export PYTHONPATH=$PYTHONPATH:/workspaces/k8s-aws-ec2/webapp

# Step 1: Run pytest with coverage for the webapp, unit, and integration tests
coverage run -m pytest tests/unit tests/integration

# Step 2: Show coverage report in terminal
coverage report

# Step 3: Generate HTML coverage report in htmlcov
coverage html -d htmlcov

echo -e "\nHTML coverage report generated at htmlcov/index.html"
