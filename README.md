# productivity-personal-suite

A lightweight, cross-platform personal productivity command-line suite for Mac/Linux. Combines calculator, notes manager, countdown timer, and file organizer into a single unified CLI application.

## Overview

A minimal yet feature-rich CLI tool designed for daily productivity tasks:
- **Calculator**: Quick arithmetic with support for advanced operations (sqrt, powers)
- **Notes**: Create, list, view, and delete text-based notes (stored locally)
- **Timer**: Countdown timer with custom messages and minute/second support
- **File Organizer**: Automatically sort files by extension into organized folders

Perfect for students, developers, and anyone looking for a lightweight productivity companion without cloud dependencies.

## Features

### 1. Calculator
- Basic arithmetic: `+`, `-`, `*`, `/`, `%`
- Advanced: `**` (exponentiation), `sqrt` (square root)
- Examples:
  - `2 + 2` → 4
  - `5 * 3` → 15
  - `2 ** 8` → 256
  - `sqrt 16` → 4.0
- Safe evaluation with restricted builtins (security-focused)

### 2. Notes Management
- **Create Notes**: Write notes with auto-formatted titles
- **List Notes**: View all saved notes with timestamps
- **View Notes**: Read full note content with formatted headers
- **Delete Notes**: Remove notes with confirmation prompt
- Storage: `~/Productivity/notes/` (auto-created)
- Format: Plain text files with title separators for readability

### 3. Timer
- **Flexible input**: Seconds (`90`) or minutes (`5m`)
- **Live countdown**: Real-time display in `MM:SS` format
- **Custom messages**: Add optional completion messages
- **Audio alert**: Bell sound when timer completes
- **Cancellable**: Press Ctrl+C to stop timer

### 4. File Organizer
- **Automatic sorting**: Moves files into extension-based subfolders
- **Recursive**: Processes all files in target directory
- **Smart naming**: Creates folders like `pdf`, `jpg`, `txt`, etc.
- **Fallback**: Files without extension go to `no_ext` folder
- **Error handling**: Skips protected files and reports failures

## Project Structure

```
productivity-personal-suite/
├── README.md                        # This file
└── productivity_personal_suite.py    # Main CLI application

Generated at runtime:
~/Productivity/
├── notes/                           # Note storage directory
│   ├── my_todo.txt
│   ├── project_ideas.txt
│   └── ...
```

## Requirements

- Python 3.6+
- macOS / Linux / WSL (cross-platform compatible)
- No external dependencies (uses only Python standard library)

## Installation

### Method 1: Direct Usage
```bash
# Clone the repository
git clone https://github.com/ritvikvr/productivity-personal-suite.git
cd productivity-personal-suite

# Run directly
python3 productivity_personal_suite.py
```

### Method 2: Add to PATH (Optional)
```bash
# Make executable
chmod +x productivity_personal_suite.py

# Create symlink or copy to /usr/local/bin
sudo cp productivity_personal_suite.py /usr/local/bin/productivity

# Now run from anywhere
productivity
```

## Usage Guide

### Main Menu
```
=== Personal Productivity Suite (CLI) ===
1) Calculator
2) Notes
3) Timer
4) File Organizer
q) Quit
Select>
```

### Calculator Examples
```
calc> 2 + 2
4

calc> 2 ** 8
256

calc> sqrt 16
4.0

calc> back
```

### Notes Examples
```
# Create a note
Notes — choose an action:
1) Create a note
2) List notes
3) View a note
4) Delete a note
notes> 1
Title: My Todo
Enter note content. Finish with a single line containing only '.'
This is my todo list
Finish project report
Review code
.
Saved: ~/Productivity/notes/My_Todo.txt
```

### Timer Examples
```
timer> 90
Message when done (optional): Work session complete!
Time left: 01:30
Time left: 01:29
... (counts down)
Time left: 00:00
Work session complete!

timer> 5m
Message when done (optional): Break time over
```

### File Organizer Examples
```
organ> ~/Downloads
Organizing: /Users/username/Downloads
Moved document.pdf -> pdf/
Moved image.jpg -> jpg/
Moved notes.txt -> txt/
Done organizing.
```

## Security & Privacy

- **No cloud sync**: All notes and data stored locally
- **Safe evaluation**: Calculator uses restricted evaluation (no shell access)
- **Local file storage**: Complete control over where files are saved
- **Offline-first**: Works completely without internet

## Customization

Edit the script to modify default directories:
```python
BASE_DIR = Path.home() / "Productivity"  # Change this line
NOTES_DIR = BASE_DIR / "notes"
```

## Troubleshooting

**"Not a valid directory" error when organizing files**
- Ensure the directory path exists and is readable
- Use absolute paths like `~/Downloads` or `/Users/username/Documents`

**Timer not working**
- Check that python3 is in your PATH: `which python3`
- Ensure the script has execute permissions: `chmod +x productivity_personal_suite.py`

**Notes not saving**
- Verify `~/Productivity/notes/` directory is writable
- Check disk space and file permissions

## Future Enhancements

- [ ] Cloud sync (optional Dropbox/Google Drive integration)
- [ ] Note categories and tags
- [ ] Recurring timers and reminders
- [ ] File organizer by date ranges
- [ ] Custom themes/colors
- [ ] Export notes to PDF/Markdown

## Author

Ritvik Verma (@ritvikvr)

## License

MIT License - Feel free to use, modify, and distribute

## Contributing

Contributions welcome! Please feel free to submit PRs for bug fixes or new features.

## Disclaimer

This tool is provided as-is for personal productivity. Users are responsible for backing up important notes. Always maintain local backups of critical information.
