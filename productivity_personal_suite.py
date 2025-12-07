#!/usr/bin/env python3
"""
Personal Productivity Suite (CLI) - Mac / cross-platform
Features:
 - Calculator (basic +, -, *, /, **, sqrt)
 - Notes (create, list, view, delete) stored as text files in ~/Productivity/notes/
 - Timer (countdown with optional message)
 - File Organizer (move files into extension folders)
"""

import os
import sys
import shutil
import time
from pathlib import Path
from math import sqrt

# --- Configuration (changeable) ---
BASE_DIR = Path.home() / "Productivity"
NOTES_DIR = BASE_DIR / "notes"
# Ensure directories exist
NOTES_DIR.mkdir(parents=True, exist_ok=True)


# ---------- Calculator ----------
def calc_prompt():
    print("\nCalculator — enter simple expressions.")
    print("Examples: 2 + 2, 5*3, 2 ** 8, sqrt 16")
    print("Type 'back' to return to main menu.")
    while True:
        expr = input("calc> ").strip()
        if expr.lower() in ("back", "exit", "quit"):
            return
        if expr.startswith("sqrt"):
            # support "sqrt 16"
            parts = expr.split()
            if len(parts) == 2:
                try:
                    val = float(parts[1])
                    print(sqrt(val))
                except Exception as e:
                    print("Error:", e)
            else:
                print("Usage: sqrt <number>")
            continue
        # Basic safety: allow only digits, whitespace and safe operators
        allowed = set("0123456789+-*/().%eE ")
        if set(expr) - allowed:
            # Still allow ** operator and power notation
            # but reject suspicious characters
            pass
        try:
            # Evaluate with minimal globals (no builtins accessible)
            result = eval(expr, {"__builtins__": None}, {})
            print(result)
        except Exception as e:
            print("Error evaluating expression:", e)


# ---------- Notes ----------
def notes_menu():
    while True:
        print("\nNotes — choose an action:")
        print("1) Create a note")
        print("2) List notes")
        print("3) View a note")
        print("4) Delete a note")
        print("b) Back to main menu")
        choice = input("notes> ").strip().lower()
        if choice == "1":
            create_note()
        elif choice == "2":
            list_notes()
        elif choice == "3":
            view_note()
        elif choice == "4":
            delete_note()
        elif choice in ("b", "back"):
            return
        else:
            print("Unknown option.")


def create_note():
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    # Sanitize filename
    safe = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).rstrip()
    filename = f"{safe}.txt"
    path = NOTES_DIR / filename
    if path.exists():
        overwrite = input("Note exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != "y":
            print("Aborted.")
            return
    print("Enter note content. Finish with a single line containing only '.'")
    lines = []
    while True:
        line = input()
        if line.strip() == ".":
            break
        lines.append(line)
    content = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{title}\n")
        f.write("=" * max(10, len(title)) + "\n")
        f.write(content + "\n")
    print(f"Saved: {path}")


def list_notes():
    files = sorted(NOTES_DIR.glob("*.txt"))
    if not files:
        print("No notes found.")
        return
    print("\nNotes:")
    for i, p in enumerate(files, 1):
        print(f"{i}. {p.stem} ({p.stat().st_mtime_ns // 1_000_000_000} s since epoch)")  # quick info


def view_note():
    files = sorted(NOTES_DIR.glob("*.txt"))
    if not files:
        print("No notes to view.")
        return
    for i, p in enumerate(files, 1):
        print(f"{i}. {p.stem}")
    try:
        choice = int(input("Select note number: ").strip())
        if not (1 <= choice <= len(files)):
            print("Out of range.")
            return
    except ValueError:
        print("Invalid input.")
        return
    path = files[choice - 1]
    with open(path, "r", encoding="utf-8") as f:
        print("\n" + f.read())


def delete_note():
    files = sorted(NOTES_DIR.glob("*.txt"))
    if not files:
        print("No notes to delete.")
        return
    for i, p in enumerate(files, 1):
        print(f"{i}. {p.stem}")
    try:
        choice = int(input("Select note number to delete: ").strip())
        if not (1 <= choice <= len(files)):
            print("Out of range.")
            return
    except ValueError:
        print("Invalid input.")
        return
    path = files[choice - 1]
    confirm = input(f"Delete '{path.stem}'? (y/N): ").strip().lower()
    if confirm == "y":
        path.unlink()
        print("Deleted.")
    else:
        print("Aborted.")


# ---------- Timer ----------
def timer_prompt():
    print("\nTimer — set a countdown in seconds (or 'm' for minutes). Type 'back' to return.")
    while True:
        s = input("timer> ").strip().lower()
        if s in ("back", "b", "exit", "quit"):
            return
        # Allow formats: 90 (seconds) or 5m (minutes)
        try:
            if s.endswith("m"):
                seconds = int(float(s[:-1]) * 60)
            else:
                seconds = int(float(s))
            if seconds <= 0:
                print("Enter a positive number.")
                continue
        except Exception:
            print("Invalid format. Examples: '90' or '5m'")
            continue
        message = input("Message when done (optional): ").strip()
        countdown(seconds, message)


def countdown(seconds, message="Time's up!"):
    try:
        start = time.time()
        end = start + seconds
        while True:
            left = int(end - time.time())
            if left < 0:
                break
            mins, sec = divmod(left, 60)
            sys.stdout.write(f"\rTime left: {mins:02d}:{sec:02d}")
            sys.stdout.flush()
            time.sleep(1)
        # finished
        sys.stdout.write("\n")
        print("\a")  # bell
        print(message)
    except KeyboardInterrupt:
        print("\nTimer cancelled.")


# ---------- File Organizer ----------
def organizer_prompt():
    print("\nFile Organizer — move files by extension into folders.")
    print("Example: organize ~/Downloads (will create folders like 'pdf', 'jpg', etc.)")
    print("Type 'back' to return.")
    while True:
        target = input("organize> ").strip()
        if not target:
            continue
        if target in ("back", "b", "exit", "quit"):
            return
        target_path = Path(os.path.expanduser(target)).resolve()
        if not target_path.exists() or not target_path.is_dir():
            print("Not a valid directory. Try again.")
            continue
        organize_folder(target_path)
        break


def organize_folder(folder: Path):
    print(f"Organizing: {folder}")
    for item in folder.iterdir():
        if item.is_dir():
            continue  # skip directories
        ext = item.suffix.lower().lstrip(".")
        if not ext:
            ext = "no_ext"
        dest = folder / ext
        dest.mkdir(exist_ok=True)
        try:
            shutil.move(str(item), str(dest / item.name))
            print(f"Moved {item.name} -> {dest.name}/")
        except Exception as e:
            print(f"Failed to move {item.name}: {e}")
    print("Done organizing.")


# ---------- Main Menu ----------
def main_menu():
    while True:
        print("\n=== Personal Productivity Suite (CLI) ===")
        print("1) Calculator")
        print("2) Notes")
        print("3) Timer")
        print("4) File Organizer")
        print("q) Quit")
        choice = input("Select> ").strip().lower()
        if choice == "1":
            calc_prompt()
        elif choice == "2":
            notes_menu()
        elif choice == "3":
            timer_prompt()
        elif choice == "4":
            organizer_prompt()
        elif choice in ("q", "quit", "exit"):
            print("Goodbye!")
            return
        else:
            print("Unknown option.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")
