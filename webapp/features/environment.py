from behave_django.environment import *
from playwright.sync_api import sync_playwright
import os
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

def before_all(context):
    # Setup Django's test database (handled by behave-django)
    pass

def before_scenario(context, scenario):
    # Set up a new browser instance for each scenario
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True)
    context.browser_context = context.browser.new_context()
    context.page = context.browser_context.new_page()

    # Clean up database for each scenario (handled by behave-django's transactions)
    # You might need to explicitly clear some data or use behave-django's fixtures/tags.
    context.client = Client()  # Use Django test client

def after_scenario(context, scenario):
    # Use Playwright
    context.browser_context.close()
    context.browser.close()
    context.playwright.stop()

def after_all(context):
    pass # Clean up after all tests if necessary
