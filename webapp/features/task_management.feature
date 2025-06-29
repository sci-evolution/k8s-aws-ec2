Feature: Task Management
  As a user
  I want to manage my tasks
  So that I can keep track of my work

  Scenario: Successfully create a new task
    Given I am on the "new task" page
    When I fill in "title" with "Buy groceries"
    And I fill in "description" with "Milk, eggs, bread, cheese"
    And I fill in "start_time" with "2025-07-01T10:00"
    And I fill in "end_time" with "2025-07-01T11:00"
    And I select "HIGH" from "priority"
    And I select "TODO" from "status"
    And I click the "Create Task" button
    Then I should be on the "tasks list" page
    And I should see "Buy groceries" in the tasks list

  Scenario: Display error when creating a task with missing title
    Given I am on the "new task" page
    When I fill in "description" with "Some description"
    And I click the "Create Task" button
    Then I should see an error message "This field is required."
    And I should still be on the "new task" page

  Scenario: Successfully view a task
    Given a task with title "View This Task" exists
    And I am on the "tasks list" page
    When I click the link for "View This Task"
    Then I should be on the "task detail" page for "View This Task"
    And I should see "View This Task" as the task title
    And I should see the description for "View This Task"
    And I should see the priority for "View This Task"
    And I should see the status for "View This Task"

  Scenario: Successfully update a task
    Given a task with title "Update This Task" exists
    And I am on the "task detail" page for "Update This Task"
    When I fill in "title" with "Updated Task Title"
    And I select "DONE" from "status"
    And I click the "Update Task" button
    Then I should be on the "task detail" page for "Updated Task Title"
    And I should see "Updated Task Title" as the task title
    And I should see "DONE" as the task status

  Scenario: Successfully delete a task
    Given a task with title "Delete This Task" exists
    And I am on the "tasks list" page
    When I click the delete button for "Delete This Task"
    And I confirm the deletion
    Then I should be on the "tasks list" page
    And I should not see "Delete This Task" in the tasks list

  Scenario: Search for tasks
    Given a task with title "Task A" exists
    And a task with title "Task B" exists
    And a task with title "Another Task C" exists
    And I am on the "tasks list" page
    When I fill in "search" with "Task"
    And I click the "Search" button
    Then I should see "Task A" in the tasks list
    And I should see "Task B" in the tasks list
    And I should not see "Another Task C" in the tasks list
