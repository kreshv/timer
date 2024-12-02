import time
import json
from datetime import datetime, timedelta
import os

class WorkTimer:
    def __init__(self, weekly_goal=100):
        self.state_file = os.path.expanduser('~/.work_timer_state.json')
        self.weekly_goal = weekly_goal
        self.load_state()

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

    def start(self):
        if not self.state['is_running']:
            self.state['is_running'] = True
            self.state['start_time'] = datetime.now().isoformat()
            self.save_state()
            print("Timer started.")
        else:
            print("Timer is already running.")

    def stop(self):
        if self.state['is_running']:
            start_time = datetime.fromisoformat(self.state['start_time'])
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.state['total_seconds'] += duration
            self.state['is_running'] = False
            self.state['start_time'] = None
            self.save_state()
            print(f"Timer stopped. Duration: {duration/3600:.2f} hours")
        else:
            print("Timer is not running.")

    def status(self):
        total_hours = self.state['total_seconds'] / 3600
        remaining_hours = max(0, self.weekly_goal - total_hours)
        
        print(f"Weekly Goal: {self.weekly_goal} hours")
        print(f"Current Week's Work: {total_hours:.2f} hours")
        print(f"Remaining Hours: {remaining_hours:.2f} hours")
        print(f"Status: {'Running' if self.state['is_running'] else 'Stopped'}")

def main():
    timer = WorkTimer()
    
    while True:
        print("\nWork Timer Menu:")
        print("1. Start Timer")
        print("2. Stop Timer")
        print("3. Check Status")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            timer.start()
        elif choice == '2':
            timer.stop()
        elif choice == '3':
            timer.status()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main() 