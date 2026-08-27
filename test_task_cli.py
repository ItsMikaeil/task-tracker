import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parent / "task_cli.py"


class TaskCliTestCase(unittest.TestCase):

    def run_cli(self, *args):
        """
        Run task_cli.py like a real user would run it.

        Example:
            run_cli("add", "Learn Python")
        is similar to:
            python3 task_cli.py add "Learn Python"
        """

        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            cwd=self.test_dir,
            capture_output=True,
            text=True
        )

    def load_tasks(self):
        """
        Read tasks.json created by the CLI.
        """

        tasks_file = Path(self.test_dir) / "tasks.json"

        with open(tasks_file, "r") as file:
            return json.load(file)

    def setUp(self):
        """
        Run before every test.

        We create a completely new temporary directory
        so tests don't modify your real tasks.json.
        """

        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = self.temp_dir.name

    def tearDown(self):
        """
        Run after every test.

        Delete the temporary directory.
        """

        self.temp_dir.cleanup()

    def test_add_task(self):
        """A task should be added successfully."""

        result = self.run_cli(
            "add",
            "Learn Python"
        )

        self.assertEqual(result.returncode, 0)

        tasks = self.load_tasks()

        self.assertEqual(len(tasks), 1)

        task = tasks[0]

        self.assertEqual(task["id"], 1)
        self.assertEqual(task["description"], "Learn Python")
        self.assertEqual(task["status"], "todo")

        self.assertIn("createdAt", task)
        self.assertIn("updatedAt", task)

    def test_add_multiple_tasks(self):
        """Multiple tasks should get unique IDs."""

        self.run_cli("add", "Learn Python")
        self.run_cli("add", "Learn FastAPI")
        self.run_cli("add", "Build website")

        tasks = self.load_tasks()

        self.assertEqual(len(tasks), 3)

        ids = [task["id"] for task in tasks]

        self.assertEqual(ids, [1, 2, 3])

    def test_list_tasks(self):
        """List should display the existing tasks."""

        self.run_cli("add", "Learn Python")
        self.run_cli("add", "Build website")

        result = self.run_cli("list")

        self.assertEqual(result.returncode, 0)

        self.assertIn("Learn Python", result.stdout)
        self.assertIn("Build website", result.stdout)

    def test_mark_in_progress(self):
        """A task should change to in-progress."""

        self.run_cli("add", "Learn Python")

        result = self.run_cli(
            "mark-in-progress",
            "1"
        )

        self.assertEqual(result.returncode, 0)

        tasks = self.load_tasks()

        self.assertEqual(
            tasks[0]["status"],
            "in-progress"
        )

    def test_mark_done(self):
        """A task should change to done."""

        self.run_cli("add", "Learn Python")

        result = self.run_cli(
            "mark-done",
            "1"
        )

        self.assertEqual(result.returncode, 0)

        tasks = self.load_tasks()

        self.assertEqual(
            tasks[0]["status"],
            "done"
        )

    def test_update_task(self):
        """Task description should be updated."""

        self.run_cli(
            "add",
            "Learn Python"
        )

        result = self.run_cli(
            "update",
            "1",
            "Learn Python deeply"
        )

        self.assertEqual(result.returncode, 0)

        tasks = self.load_tasks()

        self.assertEqual(
            tasks[0]["description"],
            "Learn Python deeply"
        )

    def test_delete_task(self):
        """A task should be deleted."""

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

        self.assertEqual(result.returncode, 0)

        tasks = self.load_tasks()

        self.assertEqual(len(tasks), 1)

        self.assertEqual(
            tasks[0]["description"],
            "Build website"
        )

    def test_list_todo_tasks(self):
        """list todo should only show todo tasks."""

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
        """list done should only show done tasks."""

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

    def test_missing_command(self):
        """Running without a command should show an error."""

        result = self.run_cli()

        self.assertIn(
            "No command",
            result.stdout
        )

    def test_add_without_description(self):
        """add without a description should fail gracefully."""

        result = self.run_cli("add")

        self.assertIn(
            "description",
            result.stdout.lower()
        )

    def test_invalid_task_id(self):
        """A non-numeric task ID should be rejected."""

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
        """Using an ID that doesn't exist should fail gracefully."""

        result = self.run_cli(
            "delete",
            "999"
        )

        self.assertIn(
            "not found",
            result.stdout.lower()
        )

    def test_invalid_status(self):
        """list should reject an invalid status."""

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


if __name__ == "__main__":
    unittest.main(verbosity=2)