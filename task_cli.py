"""
Task Tracker CLI

A simple command-line application for creating and managing tasks.

Supported commands:

    python3 task_cli.py add "Learn Python"
    python3 task_cli.py list
    python3 task_cli.py list todo
    python3 task_cli.py list in-progress
    python3 task_cli.py list done
    python3 task_cli.py update 1 "Learn Python deeply"
    python3 task_cli.py delete 1
    python3 task_cli.py mark-in-progress 1
    python3 task_cli.py mark-done 1

Tasks are stored in a local JSON file named tasks.json.
"""

from datetime import datetime
import json
import os
import sys


# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

TASKS_FILE = "tasks.json"

VALID_STATUSES = [
    "todo",
    "in-progress",
    "done"
]


# ---------------------------------------------------------
# Load tasks from tasks.json
# ---------------------------------------------------------

# If tasks.json does not exist, create it with an empty list.
#
# An empty list means:
#
# []
#
# There are currently no tasks.

if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "w") as file:
        json.dump([], file)


# Read the tasks from the JSON file.
#
# json.load() converts JSON data into Python objects.
#
# Example:
#
# JSON:
# [
#     {"id": 1, "description": "Learn Python"}
# ]
#
# becomes a Python list containing dictionaries.

try:
    with open(TASKS_FILE, "r") as file:
        tasks = json.load(file)

except json.JSONDecodeError:
    print("Error: tasks.json contains invalid JSON.")
    exit()


# Make sure the JSON contains a list.
if not isinstance(tasks, list):
    print("Error: tasks.json must contain a list of tasks.")
    exit()


# ---------------------------------------------------------
# Read command-line arguments
# ---------------------------------------------------------

# sys.argv contains the arguments entered in the terminal.
#
# Example:
#
# python3 task_cli.py add "Learn Python"
#
# sys.argv becomes:
#
# [
#     "task_cli.py",
#     "add",
#     "Learn Python"
# ]

if len(sys.argv) == 1:
    print("No command provided.")
    exit()


command = sys.argv[1]


# ---------------------------------------------------------
# ADD
# ---------------------------------------------------------

if command == "add":

    # A description is required.
    #
    # We need:
    #
    # sys.argv[0] -> task_cli.py
    # sys.argv[1] -> add
    # sys.argv[2] -> description

    if len(sys.argv) < 3:
        print("No description provided.")
        exit()

    # Ignore additional arguments.
    if len(sys.argv) > 3:
        print("Too many arguments for add command.")
        exit()

    description = sys.argv[2]

    # Reject an empty description such as:
    #
    # add "     "

    if not description.strip():
        print("Description cannot be empty.")
        exit()

    # Generate a new ID.
    #
    # If there are no tasks:
    #       ID = 1
    #
    # Otherwise:
    #       largest existing ID + 1

    new_id = 1

    if tasks:
        new_id = max(task["id"] for task in tasks) + 1

    # Get the current date and time.
    #
    # isoformat() converts datetime into a string
    # suitable for storing in JSON.

    now = datetime.now().isoformat()

    # Create the task as a Python dictionary.

    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

    # Add the task to our list.

    tasks.append(task)

    # Save the updated list back to tasks.json.

    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task added successfully with id {new_id}")


# ---------------------------------------------------------
# LIST
# ---------------------------------------------------------

if command == "list":

    # If there are no tasks, tell the user.

    if not tasks:
        print("No tasks found.")
        exit()

    # -----------------------------------------------------
    # List ALL tasks
    # -----------------------------------------------------

    if len(sys.argv) == 2:

        for task in tasks:
            print(f"ID: {task['id']}")
            print(f"Description: {task['description']}")
            print(f"Status: {task['status']}")
            print()

        exit()

    # list accepts at most one filter.
    #
    # Example:
    #
    # list done
    #
    # but not:
    #
    # list done something

    if len(sys.argv) > 3:
        print("Too many arguments for list command.")
        exit()

    # Get the requested status.

    status_filter = sys.argv[2]

    # Check whether the status is valid.

    if status_filter not in VALID_STATUSES:
        print("Invalid status.")
        exit()

    # This variable tells us whether we found
    # at least one matching task.

    found = False

    # Search through all tasks.

    for task in tasks:

        if task["status"] == status_filter:

            found = True

            print(f"ID: {task['id']}")
            print(f"Description: {task['description']}")
            print(f"Status: {task['status']}")
            print()

    # If no task matched the requested status.

    if not found:
        print(
            f"No task found with status: {status_filter}"
        )


# ---------------------------------------------------------
# MARK-DONE
# ---------------------------------------------------------

if command == "mark-done":

    # We need:
    #
    # sys.argv[0] -> task_cli.py
    # sys.argv[1] -> mark-done
    # sys.argv[2] -> task ID

    if len(sys.argv) < 3:
        print("Task Id is required.")
        exit()

    if len(sys.argv) > 3:
        print("Too many arguments for mark-done command.")
        exit()

    # Convert task ID from string to integer.

    try:
        task_id = int(sys.argv[2])

    except ValueError:
        print("Task Id must be a number.")
        exit()

    # Look for the requested task.

    found = False

    for task in tasks:

        if task_id == task["id"]:

            found = True

            task["status"] = "done"

            # Updating the status counts as updating the task,
            # so updatedAt must also change.

            task["updatedAt"] = datetime.now().isoformat()

            break

    # Task was not found.

    if not found:
        print(f"Task with ID {task_id} not found.")
        exit()

    # Save the modified tasks.

    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {task_id} marked as done.")


# ---------------------------------------------------------
# MARK-IN-PROGRESS
# ---------------------------------------------------------

if command == "mark-in-progress":

    if len(sys.argv) < 3:
        print("Task Id is required.")
        exit()

    if len(sys.argv) > 3:
        print(
            "Too many arguments for "
            "mark-in-progress command."
        )
        exit()

    try:
        task_id = int(sys.argv[2])

    except ValueError:
        print("Task Id must be a number.")
        exit()

    found = False

    for task in tasks:

        if task_id == task["id"]:

            found = True

            task["status"] = "in-progress"

            task["updatedAt"] = datetime.now().isoformat()

            break

    if not found:
        print(f"Task with ID {task_id} not found.")
        exit()

    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {task_id} marked as in-progress.")


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

if command == "update":

    # update requires:
    #
    # update <id> <new description>
    #
    # Example:
    #
    # update 1 "Learn Python deeply"

    if len(sys.argv) < 4:
        print(
            "Task ID and new description are required."
        )
        exit()

    if len(sys.argv) > 4:
        print("Too many arguments for update command.")
        exit()

    # Convert ID from string to integer.

    try:
        task_id = int(sys.argv[2])

    except ValueError:
        print("Task Id must be a number.")
        exit()

    new_description = sys.argv[3]

    # Prevent an empty description.

    if not new_description.strip():
        print("Description cannot be empty.")
        exit()

    found = False

    # Find the task.

    for task in tasks:

        if task_id == task["id"]:

            found = True

            # Change the description.

            task["description"] = new_description

            # createdAt should NOT change.
            #
            # updatedAt SHOULD change.

            task["updatedAt"] = datetime.now().isoformat()

            break

    if not found:
        print(f"Task with ID {task_id} not found.")
        exit()

    # Save the updated task list.

    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {task_id} updated successfully.")


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------

if command == "delete":

    if len(sys.argv) < 3:
        print("Task Id is required.")
        exit()

    if len(sys.argv) > 3:
        print("Too many arguments for delete command.")
        exit()

    try:
        task_id = int(sys.argv[2])

    except ValueError:
        print("Task Id must be a number.")
        exit()

    found = False

    # Find and remove the requested task.

    for task in tasks:

        if task_id == task["id"]:

            found = True

            tasks.remove(task)

            break

    if not found:
        print(f"Task with ID {task_id} not found.")
        exit()

    # Save the new list.

    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {task_id} deleted successfully.")