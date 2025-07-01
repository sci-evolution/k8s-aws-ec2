Feature: Task Management
  As a user
  I want to manage my tasks
  So that I can keep track of my work

  # CREATE
  Scenario: Successfully create a new task
    Given I am on the new task page
    When I fill in "title" with "Buy groceries"
    And I fill in "description" with "Milk, eggs, bread, cheese"
    And I select "HIGH" from "priority"
    And I select "TODO" from "status"
    And I click the "Create Task" button
    Then I should be on the tasks list page
    And I should see "Buy groceries" in the tasks list

  Scenario: Display error when creating a task with missing title
    Given I am on the new task page
    When I fill in "description" with "Some description"
    And I click the "Create Task" button
    Then I should see an error message "This field is required."
    And I should still be on the new task page

  Scenario: Display error when creating a task with invalid data
    Given I am on the new task page
    When I fill in "title" with "A"
    And I fill in "description" with "desc"
    And I fill in "start_time" with "invalid-date"
    And I click the "Create Task" button
    Then I should see an error message "Enter a valid date/time."
    And I should still be on the new task page

  Scenario: Internal error when creating a task
    Given I am on the new task page
    When I fill in "title" with "Trigger 500"
    And I click the "Create Task" button
    Then I should see an error message "Internal Server Error"
    And I should still be on the new task page

  # READ
  Scenario: Successfully view a task
    Given a task with title "View This Task" exists
    And I am on the tasks list page
    When I click the link for "View This Task"
    Then I should be on the task detail page for "View This Task"
    And I should see "View This Task" as the task title
    And I should see the description for "View This Task"
    And I should see the priority for "View This Task"
    And I should see the status for "View This Task"

  Scenario: Error when viewing a non-existent task
    Given I am on the task detail page for "non-existent-task"
    Then I should see an error message "Task not found"

  Scenario: Internal error when viewing a task
    Given a task with title "Trigger 500" exists
    And I am on the task detail page for "Trigger 500"
    Then I should see an error message "Internal Server Error"

  # UPDATE
  Scenario: Successfully update a task
    Given a task with title "Update This Task" exists
    And I am on the task detail page for "Update This Task"
    When I fill in "title" with "Updated Task Title"
    And I select "DONE" from "status"
    And I click the "Update Task" button
    Then I should be on the task detail page for "Updated Task Title"
    And I should see "Updated Task Title" as the task title
    And I should see "DONE" as the task status

  Scenario: Error when updating a non-existent task
    Given I am on the task detail page for "non-existent-task"
    When I fill in "title" with "Anything"
    And I click the "Update Task" button
    Then I should see an error message "Task not found"

  Scenario: Error when updating with invalid data
    Given a task with title "Update Invalid" exists
    And I am on the task detail page for "Update Invalid"
    When I fill in "title" with ""
    And I click the "Update Task" button
    Then I should see an error message "This field is required."

  Scenario: Internal error when updating a task
    Given a task with title "Trigger 500" exists
    And I am on the task detail page for "Trigger 500"
    When I fill in "title" with "Trigger 500"
    And I click the "Update Task" button
    Then I should see an error message "Internal Server Error"

  # DELETE
  Scenario: Successfully delete a task
    Given a task with title "Delete This Task" exists
    And I am on the tasks list page
    When I click the delete button for "Delete This Task"
    And I confirm the deletion
    Then I should be on the tasks list page
    And I should not see "Delete This Task" in the tasks list

  Scenario: Error when deleting a non-existent task
    Given I am on the tasks list page
    When I click the delete button for "non-existent-task"
    And I confirm the deletion
    Then I should see an error message "Task not found"

  Scenario: Internal error when deleting a task
    Given a task with title "Trigger 500" exists
    And I am on the tasks list page
    When I click the delete button for "Trigger 500"
    And I confirm the deletion
    Then I should see an error message "Internal Server Error"

  # SEARCH
  Scenario: Search for tasks
    Given a task with title "Task A" exists
    And a task with title "Task B" exists
    And a task with title "Another Task C" exists
    And I am on the tasks list page
    When I fill in "search" with "Task"
    And I click the "Search" button
    Then I should see "Task A" in the tasks list
    And I should see "Task B" in the tasks list
    And I should not see "Another Task C" in the tasks list

  Scenario: Error when searching with invalid input
    Given a task with title "Task A" exists
    And I am on the tasks list page
    When I fill in "search" with "!@#$%"
    And I click the "Search" button
    Then I should see an error message "Invalid search parameters"

  Scenario: Internal error when searching tasks
    Given a task with title "Trigger 500" exists
    And I am on the tasks list page
    When I fill in "search" with "Trigger 500"
    And I click the "Search" button
    Then I should see an error message "Internal Server Error"
