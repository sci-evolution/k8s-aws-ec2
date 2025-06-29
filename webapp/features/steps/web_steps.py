from behave import *

from django.urls import reverse
from django.test import Client
from tasks.models import Task # Import the Task model

use_step_matcher("re")

# --- Common Navigation Steps ---
@given('I am on the "(?P<page_name>.+)" page')
def step_impl(context, page_name):
    if page_name == "tasks list":
        context.page.goto(context.base_url + reverse('tasks:index'))
    elif page_name == "new task":
        context.page.goto(context.base_url + reverse('tasks:new_task'))
    # Add more pages here as needed
    else:
        raise ValueError(f"Unknown page name: {page_name}")

@then('I should be on the "(?P<page_name>.+)" page')
def step_impl(context, page_name):
    if page_name == "tasks list":
        expected_url_path = reverse('tasks:index')
    elif page_name == "new task":
        expected_url_path = reverse('tasks:new_task')
    # Add more pages here as needed
    else:
        raise ValueError(f"Unknown page name: {page_name}")
    # Use Playwright's wait_for_url
    context.page.wait_for_url(context.base_url + expected_url_path)
    assert expected_url_path in context.page.url

@then('I should still be on the "(?P<page_name>.+)" page')
def step_impl(context, page_name):
    if page_name == "new task":
        expected_url_path = reverse('tasks:new_task')
    # Add more pages here as needed
    else:
        raise ValueError(f"Unknown page name: {page_name}")
    # Check if the current URL path matches the expected page
    assert context.page.url.endswith(expected_url_path)

# --- Common Interaction Steps ---
@when(r"I fill in \"(?P<field_name>.+)\" with \"(?P<value>.+)\"")
def step_impl(context, field_name, value):
    # Use Playwright locators and fill
    # Adapt based on your HTML structure (name, label text, placeholder text)
    locator = context.page.locator(f'[name="{field_name}"], label:has-text("{field_name}") + input, input[placeholder="{field_name}"]')
    locator.fill(value)

@when(r"I select \"(?P<option_text>.+)\" from \"(?P<field_name>.+)\"")
def step_impl(context, option_text, field_name):
    # Use Playwright locators and select_option
    # Adapt based on your HTML structure (name, label text)
    locator = context.page.locator(f'[name="{field_name}"], label:has-text("{field_name}") + select')
    locator.select_option(label=option_text)

@when(r"I click the \"(?P<button_text>.+)\" button")
def step_impl(context, button_text):
    # Use Playwright locators and click
    # Find button by text content
    locator = context.page.locator(f'button:has-text("{button_text}")')
    locator.click()

# --- Common Assertion Steps ---
@then(r"I should see a success message \"(?P<message>.+)\"")
def step_impl(context, message):
    # Use Playwright locators and wait_for
    # Adapt based on your HTML structure (class names for success messages)
    locator = context.page.locator(f'div.alert-success:has-text("{message}"), div.message-success:has-text("{message}")')
    locator.wait_for(state='visible')
    assert message in context.page.content()

@then(r"I should see an error message \"(?P<message>.+)\"")
def step_impl(context, message):
    # Use Playwright locators and wait_for
    # Adapt based on your HTML structure (class names for error messages)
    locator = context.page.locator(f'div.alert-danger:has-text("{message}"), ul.errorlist:has-text("{message}"), span.text-danger:has-text("{message}")')
    locator.wait_for(state='visible')
    assert message in context.page.content()

@then(r"I should see \"(?P<text>.+)\" in the tasks list")
def step_impl(context, text):
    # Use Playwright locators and wait_for
    # Assuming tasks are displayed in a list or table and the text is visible
    locator = context.page.locator(f'*:has-text("{text}")')
    locator.first.wait_for(state='visible')
    assert text in context.page.content()

@then(r"I should not see \"(?P<text>.+)\" in the tasks list")
def step_impl(context, text):
    # Use Playwright locators and count
    # Assuming tasks are displayed in a list or table and the text is visible
    locator = context.page.locator(f'*:has-text("{text}")')
    assert locator.count() == 0
