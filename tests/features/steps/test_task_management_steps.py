import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from django.urls import reverse
from asgiref.sync import sync_to_async

scenarios('../task_management.feature')

@pytest.fixture(autouse=True)
def set_playwright_timeout(page):
    page.set_default_timeout(10000)  # 10 seconds

@pytest.mark.django_db
@given(parsers.cfparse('I am on the {page_name} page'))
def go_to_page(page, live_server, page_name):
    url_map = {
        'tasks list': reverse('tasks:index'),
        'new task': reverse('tasks:new_task'),
    }
    page.goto(live_server.url + url_map[page_name])

@pytest.mark.django_db
@given(parsers.cfparse('a task with title "{title}" exists'))
def create_task(title):
    from tasks.models import Task
    sync_to_async(Task.objects.create, thread_sensitive=True).sync()(
        title=title, description=f"Description for {title}", priority='LOW', status='TODO'
    )

@pytest.mark.django_db
@given(parsers.cfparse('I am on the task detail page for "{task_title}"'))
def go_to_task_detail(page, live_server, task_title):
    from tasks.models import Task
    try:
        task = sync_to_async(Task.objects.get, thread_sensitive=True).sync()(title=task_title)
        url = live_server.url + reverse('tasks:task-detail', args=[str(task.task_id)])
    except Task.DoesNotExist:
        import uuid
        url = live_server.url + reverse('tasks:task-detail', args=[str(uuid.uuid4())])
    page.goto(url)

@when(parsers.cfparse('I fill in "{field_name}" with "{value}"'))
def fill_field(page, field_name, value):
    locator = page.locator(f'[name="{field_name}"]')
    locator.fill(value)

@when(parsers.cfparse('I select "{option_text}" from "{field_name}"'))
def select_option(page, option_text, field_name):
    locator = page.locator(f'[name="{field_name}"]')
    locator.select_option(label=option_text)

@when(parsers.cfparse('I click the "{button_text}" button'))
def click_button(page, button_text):
    locator = page.locator(f'button:has-text("{button_text}")')
    locator.click()

@when(parsers.cfparse('I click the link for "{task_title}"'))
def click_task_link(page, task_title):
    locator = page.locator(f'a:has-text("{task_title}")')
    locator.click()

@when(parsers.cfparse('I click the delete button for "{task_title}"'))
def click_delete_button(page, task_title):
    locator = page.locator(f'*:has-text("{task_title}"):ancestor(tr) button:has-text("Delete")')
    locator.click()

@when('I confirm the deletion')
def confirm_deletion(page):
    page.on('dialog', lambda dialog: dialog.accept())

@then(parsers.cfparse('I should be on the {page_name} page'))
def should_be_on_page(page, live_server, page_name):
    url_map = {
        'tasks list': reverse('tasks:index'),
        'new task': reverse('tasks:new_task'),
    }
    expected_url = live_server.url + url_map[page_name]
    page.wait_for_url(expected_url)
    assert expected_url in page.url

@then(parsers.cfparse('I should still be on the {page_name} page'))
def should_still_be_on_page(page, live_server, page_name):
    url_map = {
        'new task': reverse('tasks:new_task'),
    }
    expected_url = live_server.url + url_map[page_name]
    assert page.url.endswith(expected_url)

@then(parsers.cfparse('I should see an error message "{message}"'))
def should_see_error(page, message):
    locator = page.locator(f'div.alert-danger:has-text("{message}"), ul.errorlist:has-text("{message}"), span.text-danger:has-text("{message}")')
    locator.wait_for(state='visible')
    assert message in page.content()

@then(parsers.cfparse('I should see "{text}" in the tasks list'))
def should_see_in_list(page, text):
    locator = page.locator(f'*:has-text("{text}")')
    locator.first.wait_for(state='visible')
    assert text in page.content()

@then(parsers.cfparse('I should not see "{text}" in the tasks list'))
def should_not_see_in_list(page, text):
    locator = page.locator(f'*:has-text("{text}")')
    assert locator.count() == 0

@pytest.mark.django_db
@then(parsers.cfparse('I should be on the task detail page for "{task_title}"'))
def should_be_on_task_detail(page, live_server, task_title):
    from tasks.models import Task
    task = sync_to_async(Task.objects.get, thread_sensitive=True).sync()(title=task_title)
    expected_url = live_server.url + reverse('tasks:task-detail', args=[str(task.task_id)])
    page.wait_for_url(expected_url)
    assert expected_url in page.url

@then(parsers.cfparse('I should see "{task_title}" as the task title'))
def should_see_task_title(page, task_title):
    locator = page.locator('h1')
    assert task_title in locator.text_content()

@pytest.mark.django_db
@then(parsers.cfparse('I should see the description for "{task_title}"'))
def should_see_description(page, task_title):
    from tasks.models import Task
    task = sync_to_async(Task.objects.get, thread_sensitive=True).sync()(title=task_title)
    locator = page.locator(f'*:has-text("{task.description}")')
    assert task.description in locator.text_content()

@pytest.mark.django_db
@then(parsers.cfparse('I should see the priority for "{task_title}"'))
def should_see_priority(page, task_title):
    from tasks.models import Task
    task = sync_to_async(Task.objects.get, thread_sensitive=True).sync()(title=task_title)
    locator = page.locator(f'*:has-text("{task.get_priority_display()}")')
    assert task.get_priority_display() in locator.text_content()

@pytest.mark.django_db
@then(parsers.cfparse('I should see the status for "{task_title}"'))
def should_see_status(page, task_title):
    from tasks.models import Task
    task = sync_to_async(Task.objects.get, thread_sensitive=True).sync()(title=task_title)
    locator = page.locator(f'*:has-text("{task.get_status_display()}")')
    assert task.get_status_display() in locator.text_content()

@then('I should see "DONE" as the task status')
def should_see_done_status(page):
    locator = page.locator(f'*:has-text("DONE")')
    assert "DONE" in locator.text_content()
