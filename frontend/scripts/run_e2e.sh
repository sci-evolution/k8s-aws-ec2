#!/bin/bash
# Script to run all Playwright E2E tests for the frontend

# Optionally, set environment variables here if needed
# export FRONTEND_BASE_URL="http://localhost:3000"

# Run Playwright E2E tests
npx playwright test

# Show where the Playwright HTML report is generated (if enabled in config)
echo -e "\nPlaywright E2E tests completed. See HTML report in playwright-report/ if enabled."
