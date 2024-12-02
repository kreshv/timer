# Work Timer Application

## Overview
This is a Python application to track your weekly work hours, helping you reach your goal of 100 hours per week. Now available in both CLI and GUI versions!

## Features
- Start and stop work timer
- Track total hours worked in the current week
- Automatically reset at the start of each new week
- Persistent state across sessions
- Shows remaining hours to reach your weekly goal

## Requirements
- Python 3.7+
- Tkinter (comes pre-installed with Python)

## Installation
1. Clone this repository
2. No additional dependencies required

## Usage

### Recommended Method
Run the GUI version:
```bash
python work_timer_gui.py
```

### Alternative CLI Version
If you prefer a command-line interface:
```bash
python work_timer.py
```

### GUI Interface
- Large, clear buttons to Start and Stop the timer
- Real-time updates of total and remaining hours
- Detailed time tracking (hours:minutes:seconds)
- Status indicators
- Pop-up messages for timer actions

## How It Works
- The timer automatically tracks your work hours for the current week
- State is saved in `~/.work_timer_state.json`
- Weekly goal is set to 100 hours by default (can be modified in the code)
- Resets automatically at the start of each new week

## Notes
- Make sure to stop the timer when you finish working
- The application uses your system time to calculate work duration
- Choose between CLI or GUI based on your preference