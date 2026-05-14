# Task Manager

A clean, console-based task manager built in Python. Designed as a beginner-to-intermediate portfolio project that demonstrates solid fundamentals: object-oriented design, file persistence, input validation, and a user-friendly interface.

---

## Features

- **Add tasks** with an optional description
- **View tasks** — all, pending only, or completed only
- **Mark tasks complete** with a single input
- **Delete tasks** with a confirmation prompt
- **Persistent storage** — tasks are saved to `tasks.json` and survive restarts
- **Live summary** — the menu always shows your current task counts
- **Input validation** — handles invalid input gracefully without crashing

---

## How to Run

Python 3.6 or higher is required. No external packages needed.

```bash
cd task_manager
python task_manager.py
```

---

## Project Structure

```
task_manager/
├── task_manager.py   # All application code
├── tasks.json        # Auto-created on first run (your saved tasks)
└── README.md         # This file
```

---

## Code Overview

The project is split into clear, focused components:

| Class / Function | Responsibility |
|---|---|
| `Task` | Represents a single task and handles serialisation |
| `TaskManager` | Manages the task list, file I/O, and all operations |
| `run()` | The main menu loop — ties everything together |
| `get_integer_input()` | Safe integer input helper |
| `print_header()` | Renders the app header |
| `print_menu()` | Renders the menu with a live task summary |

---

## What This Demonstrates

- **Object-oriented programming** — `Task` and `TaskManager` classes with clear responsibilities
- **File I/O** — reading and writing JSON for data persistence
- **Error handling** — invalid input, missing files, and corrupt data are all handled cleanly
- **Separation of concerns** — data logic, display logic, and input handling are kept separate
- **User experience** — confirmations before destructive actions, clear status messages, and a live summary

---

## Example Session

```
======================================================
         TASK MANAGER - Stay Organised, Stay Ahead
======================================================

  Tasks: 0 total  |  0 pending  |  0 done

  ---- MENU ----
  1. Add a task
  2. View all tasks
  ...

  Enter your choice (1-7): 1

  -- Add Task --
  Task title: Buy groceries
  Description (optional, press Enter to skip): Milk, eggs, bread

  [+] Task added: "Buy groceries" (ID: 1)
```

---

## Possible Extensions

Once you're comfortable with the code, here are ideas to take it further:

- **Due dates** — add a deadline field and sort by urgency
- **Priority levels** — low, medium, high with colour-coded output
- **Task categories** — group tasks by project or area
- **Search** — filter tasks by keyword
- **CLI arguments** — use `argparse` to allow `python task_manager.py --add "Buy milk"`
- **GUI version** — rebuild the interface using `tkinter`
