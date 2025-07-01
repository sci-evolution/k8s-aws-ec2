import { test, expect } from '@playwright/test';

test.describe('Task Management E2E', () => {
  // CREATE
  test('Successfully create a new task', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Buy groceries');
    await page.fill('textarea[name="description"]', 'Milk, eggs, bread, cheese');
    await page.selectOption('select[name="priority"]', 'HIGH');
    await page.selectOption('select[name="status"]', 'TODO');
    await page.click('button:has-text("Create Task")');
    await expect(page).toHaveURL(/\/tasks|\//);
    await expect(page.locator('*:has-text("Buy groceries")')).toBeVisible();
  });

  test('Display error when creating a task with missing title', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('textarea[name="description"]', 'Some description');
    await page.click('button:has-text("Create Task")');
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('This field is required');
    await expect(page).toHaveURL(/\/tasks\/new/);
  });

  test('Display error when creating a task with invalid data', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'A');
    await page.fill('textarea[name="description"]', 'desc');
    await page.fill('input[name="start_time"]', 'invalid-date');
    await page.click('button:has-text("Create Task")');
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('Enter a valid date/time');
    await expect(page).toHaveURL(/\/tasks\/new/);
  });

  test('Internal error when creating a task', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Trigger 500');
    await page.click('button:has-text("Create Task")');
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('Internal Server Error');
    await expect(page).toHaveURL(/\/tasks\/new/);
  });

  // READ
  test('Successfully view a task', async ({ page }) => {
    // Precondition: create the task via API or UI
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'View This Task');
    await page.fill('textarea[name="description"]', 'Description for View This Task');
    await page.selectOption('select[name="priority"]', 'HIGH');
    await page.selectOption('select[name="status"]', 'TODO');
    await page.click('button:has-text("Create Task")');
    // Go to detail page
    await page.click(`a:has-text("View This Task")`);
    await expect(page).toHaveURL(/\/tasks\//);
    await expect(page.locator('h1, h2')).toContainText('View This Task');
    await expect(page.locator('*:has-text("Description for View This Task")')).toBeVisible();
    await expect(page.locator('*:has-text("HIGH")')).toBeVisible();
    await expect(page.locator('*:has-text("TODO")')).toBeVisible();
  });

  test('Error when viewing a non-existent task', async ({ page }) => {
    await page.goto('/tasks/non-existent-task');
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('Task not found');
  });

  test('Internal error when viewing a task', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Trigger 500');
    await page.click('button:has-text("Create Task")');
    await page.goto('/tasks/trigger-500');
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('Internal Server Error');
  });

  // UPDATE
  test('Successfully update a task', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Update This Task');
    await page.fill('textarea[name="description"]', 'desc');
    await page.selectOption('select[name="priority"]', 'LOW');
    await page.selectOption('select[name="status"]', 'TODO');
    await page.click('button:has-text("Create Task")');
    await page.click(`a:has-text("Update This Task")`);
    await page.fill('input[name="title"]', 'Updated Task Title');
    await page.selectOption('select[name="status"]', 'DONE');
    await page.click('button:has-text("Update Task")');
    await expect(page.locator('h1, h2')).toContainText('Updated Task Title');
    await expect(page.locator('*:has-text("DONE")')).toBeVisible();
  });

  test('Error when updating a non-existent task', async ({ page }) => {
    await page.goto('/tasks/non-existent-task');
    await page.fill('input[name="title"]', 'Anything');
    await page.click('button:has-text("Update Task")');
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('Task not found');
  });

  test('Error when updating with invalid data', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Update Invalid');
    await page.click('button:has-text("Create Task")');
    await page.click(`a:has-text("Update Invalid")`);
    await page.fill('input[name="title"]', '');
    await page.click('button:has-text("Update Task")');
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('This field is required');
  });

  test('Internal error when updating a task', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Trigger 500');
    await page.click('button:has-text("Create Task")');
    await page.goto('/tasks/trigger-500');
    await page.fill('input[name="title"]', 'Trigger 500');
    await page.click('button:has-text("Update Task")');
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('Internal Server Error');
  });

  // DELETE
  test('Successfully delete a task', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Delete This Task');
    await page.fill('textarea[name="description"]', 'desc');
    await page.selectOption('select[name="priority"]', 'LOW');
    await page.selectOption('select[name="status"]', 'TODO');
    await page.click('button:has-text("Create Task")');
    await page.click(`button:has-text("Delete")`);
    // Confirm deletion if a dialog appears
    // await page.on('dialog', dialog => dialog.accept());
    await expect(page.locator('*:has-text("Delete This Task")')).toHaveCount(0);
  });

  test('Error when deleting a non-existent task', async ({ page }) => {
    await page.goto('/tasks');
    await page.click('button:has-text("Delete")'); // Simulate delete for non-existent
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('Task not found');
  });

  test('Internal error when deleting a task', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Trigger 500');
    await page.click('button:has-text("Create Task")');
    await page.goto('/tasks');
    await page.click('button:has-text("Delete")');
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('Internal Server Error');
  });

  // SEARCH
  test('Search for tasks', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Task A');
    await page.click('button:has-text("Create Task")');
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Task B');
    await page.click('button:has-text("Create Task")');
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Another Task C');
    await page.click('button:has-text("Create Task")');
    await page.goto('/tasks');
    await page.fill('input[name="search"]', 'Task');
    await page.click('button:has-text("Search")');
    await expect(page.locator('*:has-text("Task A")')).toBeVisible();
    await expect(page.locator('*:has-text("Task B")')).toBeVisible();
    await expect(page.locator('*:has-text("Another Task C")')).toHaveCount(0);
  });

  test('Error when searching with invalid input', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Task A');
    await page.click('button:has-text("Create Task")');
    await page.goto('/tasks');
    await page.fill('input[name="search"]', '!@#$%');
    await page.click('button:has-text("Search")');
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('Invalid search parameters');
  });

  test('Internal error when searching tasks', async ({ page }) => {
    await page.goto('/tasks/new');
    await page.fill('input[name="title"]', 'Trigger 500');
    await page.click('button:has-text("Create Task")');
    await page.goto('/tasks');
    await page.fill('input[name="search"]', 'Trigger 500');
    await page.click('button:has-text("Search")');
    await expect(page.locator('div.alert-danger, ul.errorlist, span.text-danger')).toContainText('Internal Server Error');
  });
});
