import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime, timedelta
import os

class WorkTimerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Work Timer")
        master.geometry("500x400")
        master.configure(bg='#2c3e50')  # Dark background

        # Set minimum size for the window
        master.minsize(600, 100)  # Adjust as needed to fit buttons

        # Custom style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Modern theme
        self.style.configure('TLabel', foreground='white', background='#2c3e50', font=('Helvetica', 12))
        self.style.configure('Title.TLabel', foreground='white', background='#2c3e50', font=('Helvetica', 18, 'bold'))
        
        # State file
        self.state_file = os.path.expanduser('~/.work_timer_state.json')
        self.weekly_goal = 100

        # Current session tracking
        self.current_session_start = None

        # Load state
        self.load_state()

        # Create GUI elements
        self.create_widgets()

        # Update status periodically
        self.update_status()

    def load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                # Reset if the week has changed
                week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - \
                             timedelta(days=datetime.now().weekday())
                if datetime.fromisoformat(state.get('week_start', '')) < week_start:
                    state = {
                        'week_start': week_start.isoformat(),
                        'total_seconds': 0,
                        'is_running': False,
                        'start_time': None
                    }
                self.state = state
        except (FileNotFoundError, json.JSONDecodeError):
            self.state = {
                'week_start': (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - 
                               timedelta(days=datetime.now().weekday())).isoformat(),
                'total_seconds': 0,
                'is_running': False,
                'start_time': None
            }

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)

    def create_rounded_button(self, parent, text, command):
        """Create a smaller rounded button using Canvas."""
        button_frame = tk.Frame(parent, bg='#d2b48c', bd=0)
        button_frame.pack(side=tk.LEFT, padx=10)

        canvas = tk.Canvas(button_frame, width=150, height=40, bg='#d2b48c', highlightthickness=0)
        
        # Increase the size of the ovals for rounder corners
        canvas.create_oval(0, 0, 20, 20, fill='#d2b48c', outline='#d2b48c')  # Left corner
        canvas.create_oval(130, 0, 150, 20, fill='#d2b48c', outline='#d2b48c')  # Right corner
        
        # Adjust rectangle to match the new oval sizes
        canvas.create_rectangle(20, 0, 130, 40, fill='#d2b48c', outline='#d2b48c')
        
        # Center the text
        canvas.create_text(75, 20, text=text, fill='#2c3e50', font=('Helvetica', 10, 'bold'))
        canvas.pack()

        canvas.bind("<Button-1>", lambda e: command())

    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.master, bg='#2c3e50')
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Title
        self.title_label = ttk.Label(
            main_frame, 
            text="Work Timer", 
            style='Title.TLabel'
        )
        self.title_label.pack(pady=10)

        # Status Frame
        status_frame = tk.Frame(main_frame, bg='#2c3e50')
        status_frame.pack(pady=10)

        # Total Hours Label
        self.total_hours_label = ttk.Label(
            status_frame, 
            text="Total Hours This Week: 0:00:00", 
            style='TLabel'
        )
        self.total_hours_label.pack()

        # Current Session Label
        self.session_label = ttk.Label(
            status_frame, 
            text="Current Session: 0:00:00", 
            style='TLabel'
        )
        self.session_label.pack()

        # Remaining Hours Label
        self.remaining_hours_label = ttk.Label(
            status_frame, 
            text="Remaining Hours: 100:00:00", 
            style='TLabel'
        )
        self.remaining_hours_label.pack()

        # Status Label
        self.status_label = ttk.Label(
            status_frame, 
            text="Status: Stopped", 
            style='TLabel'
        )
        self.status_label.pack()

        # Button Frame
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(pady=20)

        # Create buttons
        self.create_rounded_button(button_frame, "Start Timer", self.start_timer)
        self.create_rounded_button(button_frame, "Stop Timer", self.stop_timer)
        self.create_rounded_button(button_frame, "Reset Timer", self.reset_timer)

    def start_timer(self):
        if not self.state['is_running']:
            self.state['is_running'] = True
            self.state['start_time'] = datetime.now().isoformat()
            self.current_session_start = datetime.now()
            self.save_state()
            self.update_status()
            messagebox.showinfo("Timer", "Timer started.")
        else:
            messagebox.showwarning("Warning", "Timer is already running.")

    def stop_timer(self):
        if self.state['is_running']:
            start_time = datetime.fromisoformat(self.state['start_time'])
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.state['total_seconds'] += duration
            self.state['is_running'] = False
            self.state['start_time'] = None
            self.current_session_start = None
            self.save_state()
            self.update_status()
            messagebox.showinfo("Timer", f"Timer stopped. Duration: {self.format_seconds(duration)}")
        else:
            messagebox.showwarning("Warning", "Timer is not running.")

    def reset_timer(self):
        """Reset the timer and total hours."""
        self.state['total_seconds'] = 0
        self.state['is_running'] = False
        self.state['start_time'] = None
        self.current_session_start = None
        self.save_state()
        self.update_status()
        messagebox.showinfo("Timer", "Timer has been reset.")

    def format_seconds(self, total_seconds):
        """Convert seconds to hours:minutes:seconds format"""
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    def update_status(self):
        total_hours = self.state['total_seconds'] / 3600
        remaining_hours = max(0, self.weekly_goal - total_hours)
        
        # Calculate current session duration if timer is running
        current_session_duration = 0
        if self.state['is_running'] and self.current_session_start:
            current_session_duration = (datetime.now() - self.current_session_start).total_seconds()
        
        # Update labels
        self.total_hours_label.config(
            text=f"Total Hours This Week: {self.format_seconds(self.state['total_seconds'])}"
        )
        self.session_label.config(
            text=f"Current Session: {self.format_seconds(current_session_duration)}"
        )
        self.remaining_hours_label.config(
            text=f"Remaining Hours: {self.format_seconds(remaining_hours * 3600)}"
        )
        self.status_label.config(
            text=f"Status: {'Running' if self.state['is_running'] else 'Stopped'}"
        )

        # Schedule next update
        self.master.after(1000, self.update_status)

def main():
    root = tk.Tk()
    app = WorkTimerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main() 