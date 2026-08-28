"""
Automated tests for Task Tracker CLI.

The tests run the real task_cli.py program using subprocess.

Each test gets its own temporary directory so the real
tasks.json file is never modified.

Run:

    python3 -m unittest -v test_task_cli.py
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


# ---------------------------------------------------------
# Find task_cli.py
# ---------------------------------------------------------

# __file__ = path of this test file.
#
# .parent = project directory.
#
# / "task_cli.py" = path to the application.

SCRIPT_PATH = Path(__file__).parent / "task_cli.py"


class TaskCliTestCase(unittest.TestCase):

    # -----------------------------------------------------
    # Helper: run the CLI
    # -----------------------------------------------------

    def run_cli(self, *args):
        """
        Run task_cli.py like a real user.

        Example:

            self.run_cli("add", "Learn Python")

        is equivalent to:

            python3 task_cli.py add "Learn Python"

        The command is executed inside the temporary
        test directory.
        """

        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                *args
            ],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )

    # -----------------------------------------------------
    # Helper: read tasks.json
    # -----------------------------------------------------

    def load_tasks(self):
        """
        Read tasks.json from the temporary test directory.

        Returns:
            list: tasks stored by the application.
        """

        tasks_file = Path(self.test_dir) / "tasks.json"

        with open(tasks_file, "r") as file:
            return json.load(file)

    # -----------------------------------------------------
    # Setup
    # -----------------------------------------------------

    def setUp(self):
        """
        Create a fresh temporary directory before every test.

        This prevents tests from affecting each other and
        protects the real tasks.json file.
        """

        self.temp_dir = tempfile.TemporaryDirectory()

        self.test_dir = self.temp_dir.name

    # -----------------------------------------------------
    # Teardown
    # -----------------------------------------------------

    def tearDown(self):
        """
        Delete the temporary directory after every test.
        """

        self.temp_dir.cleanup()

    # -----------------------------------------------------
    # ADD TESTS
    # -----------------------------------------------------

    def test_add_task(self):
        """
        Adding one task should create a valid task.
        """

        result = self.run_cli(
            "add",
            "Learn Python"
        )

        # Program should finish successfully.
        self.assertEqual(
            result.returncode,
            0
        )

        tasks = self.load_tasks()

        # Exactly one task should exist.
        self.assertEqual(
            len(tasks),
            1
        )

        task = tasks[0]

        self.assertEqual(
            task["id"],
            1
        )

        self.assertEqual(
            task["description"],
            "Learn Python"
        )

        self.assertEqual(
            task["status"],
            "todo"
        )

        self.assertIn(
            "createdAt",
            task
        )

        self.assertIn(
            "updatedAt",
            task
        )

    def test_add_multiple_tasks(self):
        """
        Multiple tasks should receive unique sequential IDs.
        """

        self.run_cli(
            "add",
            "Learn Python"
        )

        self.run_cli(
            "add",
            "Learn FastAPI"
        )

        self.run_cli(
            "add",
            "Build website"
        )

        tasks = self.load_tasks()

        self.assertEqual(
            len(tasks),
            3
        )

        ids = [
            task["id"]
            for task in tasks
        ]

        self.assertEqual(
            ids,
            [1, 2, 3]
        )

    def test_add_without_description(self):
        """
        add without a description should fail gracefully.
        """

        result = self.run_cli("add")

        self.assertIn(
            "description",
            result.stdout.lower()
        )

    def test_add_empty_description(self):
        """
        Whitespace-only descriptions should be rejected.
        """

        result = self.run_cli(
            "add",
            "   "
        )

        self.assertIn(
            "description",
            result.stdout.lower()
        )

    # -----------------------------------------------------
    # LIST TESTS
    # -----------------------------------------------------

    def test_list_tasks(self):
        """
        list should display all existing tasks.
        """

        self.run_cli(
            "add",
            "Learn Python"
        )

        self.run_cli(
            "add",
            "Build website"
        )

        result = self.run_cli("list")

        self.assertEqual(
            result.returncode,
            0
        )

        self.assertIn(
            "Learn Python",
            result.stdout
        )

        self.assertIn(
            "Build website",
            result.stdout
        )

    def test_list_todo_tasks(self):
        """
        list todo should display only todo tasks.
        """

        self.run_cli(
            "add",
            "Learn Python"
        )

        self.run_cli(
            "add",
            "Build website"
        )

        self.run_cli(
            "mark-done",
            "1"
        )

        result = self.run_cli(
            "list",
            "todo"
        )

        self.assertIn(
            "Build website",
            result.stdout
        )

        self.assertNotIn(
            "Learn Python",
            result.stdout
        )

    def test_list_done_tasks(self):
        """
        list done should display only done tasks.
        """

        self.run_cli(
            "add",
            "Learn Python"
        )

        self.run_cli(
            "add",
            "Build website"
        )

        self.run_cli(
            "mark-done",
            "1"
        )

        result = self.run_cli(
            "list",
            "done"
        )

        self.assertIn(
            "Learn Python",
            result.stdout
        )

        self.assertNotIn(
            "Build website",
            result.stdout
        )

    def test_invalid_status(self):
        """
        An invalid status should be rejected.
        """

        self.run_cli(
            "add",
            "Learn Python"
        )

        result = self.run_cli(
            "list",
            "banana"
        )

        self.assertIn(
            "invalid status",
            result.stdout.lower()
        )

    # -----------------------------------------------------
    # STATUS TESTS
    # -----------------------------------------------------

    def test_mark_in_progress(self):
        """
        A task should change to in-progress.
        """

        self.run_cli(
            "add",
            "Learn Python"
        )

        result = self.run_cli(
            "mark-in-progress",
            "1"
        )

        self.assertEqual(
            result.returncode,
            0
        )

        tasks = self.load_tasks()

        self.assertEqual(
            tasks[0]["status"],
            "in-progress"
        )

    def test_mark_done(self):
        """
        A task should change to done.
        """

        self.run_cli(
            "add",
            "Learn Python"
        )

        result = self.run_cli(
            "mark-done",
            "1"
        )

        self.assertEqual(
            result.returncode,
            0
        )

        tasks = self.load_tasks()

        self.assertEqual(
            tasks[0]["status"],
            "done"
        )

    # -----------------------------------------------------
    # UPDATE TESTS
    # -----------------------------------------------------

    def test_update_task(self):
        """
        update should change the task description.
        """

        self.run_cli(
            "add",
            "Learn Python"
        )

        result = self.run_cli(
            "update",
            "1",
            "Learn Python deeply"
        )

        self.assertEqual(
            result.returncode,
            0
        )

        tasks = self.load_tasks()

        self.assertEqual(
            tasks[0]["description"],
            "Learn Python deeply"
        )

    def test_update_changes_updated_at(self):
        """
        Updating a task should change updatedAt
        while keeping createdAt unchanged.
        """

        # -----------------------------
        # Arrange
        # -----------------------------

        self.run_cli(
            "add",
            "Learn Python"
        )

        tasks_before = self.load_tasks()

        created_at_before = (
            tasks_before[0]["createdAt"]
        )

        updated_at_before = (
            tasks_before[0]["updatedAt"]
        )

        # -----------------------------
        # Act
        # -----------------------------

        self.run_cli(
            "update",
            "1",
            "Learn Python deeply"
        )

        # -----------------------------
        # Assert
        # -----------------------------

        tasks_after = self.load_tasks()

        self.assertEqual(
            tasks_after[0]["createdAt"],
            created_at_before
        )

        self.assertNotEqual(
            tasks_after[0]["updatedAt"],
            updated_at_before
        )

    # -----------------------------------------------------
    # DELETE TESTS
    # -----------------------------------------------------

    def test_delete_task(self):
        """
        delete should remove the requested task.
        """

        self.run_cli(
            "add",
            "Learn Python"
        )

        self.run_cli(
            "add",
            "Build website"
        )

        result = self.run_cli(
            "delete",
            "1"
        )

        self.assertEqual(
            result.returncode,
            0
        )

        tasks = self.load_tasks()

        self.assertEqual(
            len(tasks),
            1
        )

        self.assertEqual(
            tasks[0]["description"],
            "Build website"
        )

    # -----------------------------------------------------
    # ERROR HANDLING TESTS
    # -----------------------------------------------------

    def test_missing_command(self):
        """
        Running the program without a command
        should show an error message.
        """

        result = self.run_cli()

        self.assertIn(
            "No command",
            result.stdout
        )

    def test_invalid_task_id(self):
        """
        A non-numeric task ID should be rejected.
        """

        self.run_cli(
            "add",
            "Learn Python"
        )

        result = self.run_cli(
            "delete",
            "hello"
        )

        self.assertIn(
            "number",
            result.stdout.lower()
        )

    def test_nonexistent_task(self):
        """
        An ID that does not exist should be rejected.
        """

        result = self.run_cli(
            "delete",
            "999"
        )

        self.assertIn(
            "not found",
            result.stdout.lower()
        )

    def test_update_without_description(self):
        """
        update without a new description should fail.
        """

        self.run_cli(
            "add",
            "Learn Python"
        )

        result = self.run_cli(
            "update",
            "1"
        )

        self.assertIn(
            "description",
            result.stdout.lower()
        )


# ---------------------------------------------------------
# Run tests
# ---------------------------------------------------------

if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )