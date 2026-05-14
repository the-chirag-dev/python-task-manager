"""
Task Manager - A beginner-friendly console application
Author: Portfolio Project
Description: Manage your daily tasks with add, view, complete, and delete features.
"""

import json
import os
from datetime import datetime


DATA_FILE = "tasks.json"


class Task:
    """Represents a single task."""

    def __init__(self, task_id, title, description=""):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        """Convert task to a dictionary for saving to file."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        """Create a Task object from a dictionary (loaded from file)."""
        task = Task(data["task_id"], data["title"], data["description"])
        task.completed = data["completed"]
        task.created_at = data["created_at"]
        return task


class TaskManager:
    """Handles all task operations: add, view, complete, and delete."""

    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file if it exists."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as file:
                    data = json.load(file)
                    self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
                    self.next_id = data.get("next_id", 1)
            except (json.JSONDecodeError, KeyError):
                print("Warning: Could not read saved tasks. Starting fresh.")
                self.tasks = []
                self.next_id = 1

    def save_tasks(self):
        """Save all tasks to the JSON file."""
        data = {
            "tasks": [task.to_dict() for task in self.tasks],
            "next_id": self.next_id,
        }
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=2)

    def add_task(self, title, description=""):
        """Add a new task to the list."""
        if not title.strip():
            print("\n  [!] Task title cannot be empty.")
            return

        task = Task(self.next_id, title.strip(), description.strip())
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        print(f"\n  [+] Task added: \"{task.title}\" (ID: {task.task_id})")

    def view_tasks(self, filter_mode="all"):
        """Display tasks based on filter: 'all', 'pending', or 'completed'."""
        if filter_mode == "pending":
            tasks_to_show = [t for t in self.tasks if not t.completed]
            label = "Pending Tasks"
        elif filter_mode == "completed":
            tasks_to_show = [t for t in self.tasks if t.completed]
            label = "Completed Tasks"
        else:
            tasks_to_show = self.tasks
            label = "All Tasks"

        print(f"\n  {'=' * 50}")
        print(f"  {label} ({len(tasks_to_show)} found)")
        print(f"  {'=' * 50}")

        if not tasks_to_show:
            print("  No tasks to display.")
        else:
            for task in tasks_to_show:
                status = "[DONE]" if task.completed else "[    ]"
                print(f"\n  {status} #{task.task_id} - {task.title}")
                if task.description:
                    print(f"         Note: {task.description}")
                print(f"         Created: {task.created_at}")

        print(f"  {'=' * 50}")

    def mark_complete(self, task_id):
        """Mark a task as completed by its ID."""
        task = self._find_task(task_id)
        if task is None:
            print(f"\n  [!] No task found with ID {task_id}.")
            return

        if task.completed:
            print(f"\n  [!] Task #{task_id} is already marked as complete.")
            return

        task.completed = True
        self.save_tasks()
        print(f"\n  [✓] Task #{task_id} marked as complete: \"{task.title}\"")

    def delete_task(self, task_id):
        """Delete a task by its ID."""
        task = self._find_task(task_id)
        if task is None:
            print(f"\n  [!] No task found with ID {task_id}.")
            return

        confirm = input(f"\n  Delete \"{task.title}\"? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.tasks.remove(task)
            self.save_tasks()
            print(f"\n  [-] Task #{task_id} deleted.")
        else:
            print("\n  Deletion cancelled.")

    def _find_task(self, task_id):
        """Internal helper: find a task by its ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_summary(self):
        """Return a quick summary of task counts."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed
        return total, completed, pending


def get_integer_input(prompt):
    """Prompt the user for an integer, handling invalid input gracefully."""
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("  [!] Please enter a valid number.")


def print_header():
    """Print the application header."""
    print("\n" + "=" * 54)
    print("         TASK MANAGER - Stay Organised, Stay Ahead")
    print("=" * 54)


def print_menu(manager):
    """Print the main menu with a live task summary."""
    total, completed, pending = manager.get_summary()
    print(f"\n  Tasks: {total} total  |  {pending} pending  |  {completed} done")
    print("\n  ---- MENU ----")
    print("  1. Add a task")
    print("  2. View all tasks")
    print("  3. View pending tasks")
    print("  4. View completed tasks")
    print("  5. Mark a task complete")
    print("  6. Delete a task")
    print("  7. Quit")
    print()


def run():
    """Main application loop."""
    manager = TaskManager()
    print_header()

    while True:
        print_menu(manager)
        choice = input("  Enter your choice (1-7): ").strip()

        if choice == "1":
            print("\n  -- Add Task --")
            title = input("  Task title: ")
            description = input("  Description (optional, press Enter to skip): ")
            manager.add_task(title, description)

        elif choice == "2":
            manager.view_tasks("all")

        elif choice == "3":
            manager.view_tasks("pending")

        elif choice == "4":
            manager.view_tasks("completed")

        elif choice == "5":
            print("\n  -- Mark Complete --")
            manager.view_tasks("pending")
            task_id = get_integer_input("  Enter task ID to mark complete: ")
            manager.mark_complete(task_id)

        elif choice == "6":
            print("\n  -- Delete Task --")
            manager.view_tasks("all")
            task_id = get_integer_input("  Enter task ID to delete: ")
            manager.delete_task(task_id)

        elif choice == "7":
            print("\n  Goodbye! Your tasks have been saved.\n")
            break

        else:
            print("\n  [!] Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    run()
