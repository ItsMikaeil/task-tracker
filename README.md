
````markdown
# Task Tracker CLI

A simple command-line task tracker built with Python.

This project was created as a practical learning exercise to practice Python, command-line arguments, JSON file storage, filesystem operations, error handling, and automated testing.

## Features

- Add tasks
- Update tasks
- Delete tasks
- Mark tasks as `in-progress`
- Mark tasks as `done`
- List all tasks
- List tasks by status
- Store tasks in a JSON file
- Automatically create `tasks.json` if it does not exist
- Basic error handling and input validation
- Automated tests using Python's built-in `unittest` framework

## Task Structure

Each task contains:

```json
{
    "id": 1,
    "description": "Learn Python",
    "status": "todo",
    "createdAt": "2026-08-28T12:00:00",
    "updatedAt": "2026-08-28T12:00:00"
}
````

### Task Properties

| Property      | Description                                  |
| ------------- | -------------------------------------------- |
| `id`          | Unique identifier for the task               |
| `description` | Description of the task                      |
| `status`      | `todo`, `in-progress`, or `done`             |
| `createdAt`   | Date and time when the task was created      |
| `updatedAt`   | Date and time when the task was last updated |

## Requirements

* Python 3
* No external Python packages are required

The project uses only Python's standard library.

## Installation

Clone the repository:

```bash
git clone https://github.com/ItsMikaeil/task-tracker.git
```

Move into the project directory:

```bash
cd task-tracker
```

## Usage

### Add a task

```bash
python3 task_cli.py add "Buy groceries"
```

Example output:

```text
Task added successfully with id 1
```

### List all tasks

```bash
python3 task_cli.py list
```

### List tasks by status

List `todo` tasks:

```bash
python3 task_cli.py list todo
```

List `in-progress` tasks:

```bash
python3 task_cli.py list in-progress
```

List `done` tasks:

```bash
python3 task_cli.py list done
```

### Mark a task as in-progress

```bash
python3 task_cli.py mark-in-progress 1
```

### Mark a task as done

```bash
python3 task_cli.py mark-done 1
```

### Update a task

```bash
python3 task_cli.py update 1 "Buy groceries and cook dinner"
```

### Delete a task

```bash
python3 task_cli.py delete 1
```

## Running the Tests

The project includes automated tests written with Python's built-in `unittest` framework.

Run all tests with:

```bash
python3 -m unittest discover -v
```

The tests cover:

* Adding tasks
* Adding multiple tasks and generating IDs
* Listing tasks
* Filtering tasks by status
* Updating tasks
* Deleting tasks
* Marking tasks as `done`
* Marking tasks as `in-progress`
* Missing arguments
* Invalid task IDs
* Non-existent task IDs
* Invalid statuses

The tests use temporary directories so the real `tasks.json` file is not modified during testing.

## Project Structure

```text
task-tracker/
│
├── task_cli.py        # Main CLI application
├── test_task_cli.py   # Automated tests
├── .gitignore         # Ignored files
└── README.md          # Project documentation
```

`tasks.json` is created locally by the application and is ignored by Git.

## What I Practiced

This project helped me practice:

* Python command-line applications
* `sys.argv`
* File handling with `open()`
* JSON with `json.load()` and `json.dump()`
* Filesystem operations
* Dictionaries and lists
* Loops and conditional statements
* Exception handling with `try` / `except`
* Working with dates and times using `datetime`
* Automated testing with `unittest`
* Running CLI programs from tests with `subprocess`
* Using temporary test environments
* Git and GitHub workflow

## Project Status

This is a small educational project built to strengthen practical Python and software development skills.

Future improvements may include:

* Refactoring repeated code
* Improving the CLI interface
* Packaging the application as a real `task-cli` command
* Adding more comprehensive tests
* Improving project architecture
