#!/bin/bash
# Script to run Django acceptance (pytest-bdd) tests with Playwright and environment variables

# Set environment variables for Django settings
export BACKEND_DEBUG=1
export BACKEND_SECRET_KEY="django-insecure-ml3@$n2r2$e0hsx=q!0i5x88$nwcpj(d0t7rqfi4b9@-@))#(!"
export BACKEND_ALLOWED_HOSTS="localhost,127.0.0.1"

# Add Django project root to PYTHONPATH for all apps
export PYTHONPATH=$PYTHONPATH:/workspaces/k8s-aws-ec2/backend

# Set Django settings module
export DJANGO_SETTINGS_MODULE=todo.settings

# Step 1: Install Playwright browsers if not already installed
python3 -m playwright install

# Step 2: Run pytest with BDD features (located in tests/features)
pytest --tb=short tests/features

echo "\nAcceptance tests completed."
