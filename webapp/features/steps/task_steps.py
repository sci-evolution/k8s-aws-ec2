from behave import *
from django.urls import reverse
from tasks.models import Task

use_step_matcher("re")

@given(r'a task with title "(?P<title>.+)" exists')
def step_impl(context, title):
    # Create a task directly in the database for setup
    Task.objects.create(title=title, description=f"Description for {title}", priority='LOW', status='TODO')

@when(r"I click the link for \"(?P<task_title>.+)\"")
def step_impl(context, task_title):
    # Use Playwright locators and click
    # Find the link for the task by its title and click it
    locator = context.page.locator(f'a:has-text("{task_title}")')
    locator.click()

@when(r"I click the delete button for \"(?P<task_title>.+)\"")
def step_impl(context, task_title):
    # Use Playwright locators and click
    # Find the delete button associated with the task and click it
    # This assumes there's a way to identify the delete button for a specific task, e.g., by data attributes or relative to the task title.
    # You might need to adjust the locator based on your HTML structure.
    locator = context.page.locator(f'*:has-text("{task_title}"):ancestor(tr) button:has-text("Delete")') # Example locator for a table row
    locator.click()

@when(r'I confirm the deletion')
def step_impl(context):
    # Handle the browser's confirmation dialog using Playwright
    context.page.on('dialog', lambda dialog: dialog.accept())

@then(r"I should be on the \"task detail\" page for \"(?P<task_title>.+)\"")
def step_impl(context, task_title):
    # Find the task by title to get its ID
    task = Task.objects.get(title=task_title)
    expected_url_path = reverse('tasks:task-detail', args=[task.task_id])
    # Use Playwright's wait_for_url
    context.page.wait_for_url(context.base_url + expected_url_path)
    assert expected_url_path in context.page.url

@then(r"I should see \"(?P<task_title>.+)\" as the task title")
def step_impl(context, task_title):
    # Verify the task title is displayed on the detail page using Playwright
    # Adjust locator based on your HTML structure
    locator = context.page.locator('h1') # Example: Assuming title is in an h1 tag
    assert task_title in locator.text_content()

@then(r"I should see the description for \"(?P<task_title>.+)\"")
def step_impl(context, task_title):
    # Verify the task description is displayed on the detail page using Playwright
    task = Task.objects.get(title=task_title)
    # Adjust locator based on your HTML structure
    locator = context.page.locator(f'*:has-text("{task.description}")') # Example: Assuming description text is directly visible
    assert task.description in locator.text_content()

@then(r"I should see the priority for \"(?P<task_title>.+)\"")
def step_impl(context, task_title):
    # Verify the task priority is displayed on the detail page using Playwright
    task = Task.objects.get(title=task_title)
    # Adjust locator based on your HTML structure
    locator = context.page.locator(f'*:has-text("{task.get_priority_display()}")') # Example: Assuming priority display text is directly visible
    assert task.get_priority_display() in locator.text_content()

@then(r"I should see the status for \"(?P<task_title>.+)\"")
def step_impl(context, task_title):
    # Verify the task status is displayed on the detail page using Playwright
    task = Task.objects.get(title=task_title)
    # Adjust locator based on your HTML structure
    locator = context.page.locator(f'*:has-text("{task.get_status_display()}")') # Example: Assuming status display text is directly visible
    assert task.get_status_display() in locator.text_content()
