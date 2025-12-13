import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import os
import time
from datetime import datetime

class LootTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Entropia Loot Tracker")
        self.root.geometry("500x600")
        
        self.total_value = 0.0
        self.shrapnel_value = 0.0
        self.item_value = 0.0
        self.loot_count = 0
        self.shrapnel_drop_count = 0
        self.last_loot_time = None
        self.start_time = None
        self.skills = {} # Dictionary to store skill/attribute gains
        
        self.is_tracking = False
        self.is_mini_mode = False
        self.file_handle = None
        self.log_file_path = r"C:\Users\enjia\OneDrive\Documents\Entropia Universe\chat.log"

        # Create Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)

        # Tab 1: Loot & Efficiency
        self.tab_loot = tk.Frame(self.notebook)
        self.notebook.add(self.tab_loot, text='Loot & Efficiency')

        # Tab 2: Skills
        self.tab_skills = tk.Frame(self.notebook)
        self.notebook.add(self.tab_skills, text='Skills')

        # --- Tab 1 Content ---
        self.label_title = tk.Label(self.tab_loot, text="Total Loot Value (Session)", font=("Arial", 14))
        self.label_title.pack(pady=5)

        self.label_value = tk.Label(self.tab_loot, text="0.00 PED", font=("Arial", 24, "bold"), fg="green")
        self.label_value.pack(pady=5)

        # Breakdown labels
        self.breakdown_frame = tk.Frame(self.tab_loot)
        self.breakdown_frame.pack(pady=5)
        
        self.label_shrapnel = tk.Label(self.breakdown_frame, text="Shrapnel: 0.00 PED", font=("Arial", 11), fg="gray")
        self.label_shrapnel.pack()
        
        self.label_avg_shrapnel = tk.Label(self.breakdown_frame, text="Avg Shrapnel: 0.00 PED", font=("Arial", 9), fg="darkgray")
        self.label_avg_shrapnel.pack()
        
        self.label_items = tk.Label(self.breakdown_frame, text="Items: 0.00 PED", font=("Arial", 11), fg="blue")
        self.label_items.pack()

        # Hourly Rates
        self.rates_frame = tk.Frame(self.tab_loot)
        self.rates_frame.pack(pady=5)
        self.label_duration = tk.Label(self.rates_frame, text="Duration: 00:00:00", font=("Arial", 10))
        self.label_duration.pack()
        self.label_hourly_profit = tk.Label(self.rates_frame, text="Loot/Hr: 0.00 PED", font=("Arial", 10))
        self.label_hourly_profit.pack()

        self.btn_frame = tk.Frame(self.tab_loot)
        self.btn_frame.pack(pady=10)

        self.btn_select_file = tk.Button(self.btn_frame, text="Select Log File", command=self.select_file)
        self.btn_select_file.grid(row=0, column=0, padx=5)

        self.btn_reset = tk.Button(self.btn_frame, text="Reset", command=self.reset_tracker)
        self.btn_reset.grid(row=0, column=1, padx=5)
        
        self.btn_mini = tk.Button(self.btn_frame, text="Mini Mode", command=self.toggle_mini_mode)
        self.btn_mini.grid(row=0, column=2, padx=5)
        
        self.status_label = tk.Label(root, text="Status: Stopped", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # --- Tab 2 Content (Skills) ---
        self.skills_tree = ttk.Treeview(self.tab_skills, columns=('Skill', 'Gain'), show='headings')
        self.skills_tree.heading('Skill', text='Skill / Attribute')
        self.skills_tree.heading('Gain', text='Total Gain')
        self.skills_tree.pack(expand=True, fill='both', padx=5, pady=5)

        # Regex for loot
        # Example: 2025-12-09 18:14:54 [System] [] You received Skumtomte Candy x (5) Value: 0.0500 PED
        self.loot_pattern = re.compile(r'\[System\] \[\] You received .+ Value: ([\d\.]+) PED')
        self.timestamp_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
        
        # Regex for skills/attributes
        # You have gained 1.1051 experience in your Botany skill
        self.skill_pattern = re.compile(r'You have gained ([\d\.]+) experience in your (.+) skill')
        # You have gained 0.3969 Alertness
        self.attr_pattern = re.compile(r'You have gained ([\d\.]+) ([A-Za-z]+)$')

        # Start tracking automatically if default file exists
        if os.path.exists(self.log_file_path):
            self.start_tracking()
        else:
            self.status_label.config(text="Status: Log file not found. Please select file.")

        # Mini Mode UI
        self.mini_frame = tk.Frame(root, bg='black')
        self.label_mini = tk.Label(self.mini_frame, text="0.00 PED", font=("Arial", 12, "bold"), fg="#00ff00", bg="black")
        self.label_mini.pack(expand=True, fill='both')
        
        # Bind events for mini mode
        self.label_mini.bind("<Button-1>", self.start_move)
        self.label_mini.bind("<B1-Motion>", self.do_move)
        self.label_mini.bind("<Double-Button-1>", self.toggle_mini_mode)

    def select_file(self):
        filename = filedialog.askopenfilename(
            initialdir=os.path.dirname(self.log_file_path),
            title="Select chat.log",
            filetypes=(("Log files", "*.log"), ("All files", "*.*"))
        )
        if filename:
            self.log_file_path = filename
            self.reset_tracker()
            self.start_tracking()

    def start_tracking(self):
        if self.file_handle:
            self.file_handle.close()
        
        try:
            self.file_handle = open(self.log_file_path, 'r', encoding='utf-8')
            # Seek to the end of the file to read only new messages
            self.file_handle.seek(0, 2)
            self.is_tracking = True
            self.status_label.config(text=f"Tracking: {os.path.basename(self.log_file_path)}")
            self.root.after(100, self.read_log_update)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")
            self.status_label.config(text="Status: Error opening file")

    def reset_tracker(self):
        self.total_value = 0.0
        self.shrapnel_value = 0.0
        self.item_value = 0.0
        self.loot_count = 0
        self.shrapnel_drop_count = 0
        self.last_loot_time = None
        self.start_time = None
        self.skills = {}
        
        # Clear treeview
        for item in self.skills_tree.get_children():
            self.skills_tree.delete(item)
            
        self.update_display()

    def toggle_mini_mode(self, event=None):
        if not self.is_mini_mode:
            # Switch to Mini
            self.normal_geometry = self.root.geometry()
            self.is_mini_mode = True
            
            # Hide main widgets
            self.notebook.pack_forget()
            self.status_label.pack_forget()
            
            # Configure window
            self.root.overrideredirect(True)
            self.root.attributes('-topmost', True)
            
            # Calculate position (Top Middle)
            screen_width = self.root.winfo_screenwidth()
            width = 128
            height = 32
            x = (screen_width - width) // 2
            y = 0 
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            
            # Show mini widgets
            self.mini_frame.pack(expand=True, fill='both')
            self.update_display()
            
        else:
            # Switch to Normal
            self.is_mini_mode = False
            
            # Hide mini widgets
            self.mini_frame.pack_forget()
            
            # Restore window
            self.root.overrideredirect(False)
            self.root.attributes('-topmost', False)
            self.root.geometry(self.normal_geometry)
            
            # Show main widgets
            self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
            self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_display(self):
        self.label_value.config(text=f"{self.total_value:.2f} PED")
        self.label_mini.config(text=f"{self.total_value:.2f} PED")
        self.label_shrapnel.config(text=f"Shrapnel: {self.shrapnel_value:.2f} PED")
        
        if self.shrapnel_drop_count > 0:
            avg_shrap = self.shrapnel_value / self.shrapnel_drop_count
            self.label_avg_shrapnel.config(text=f"Avg Shrapnel: {avg_shrap:.2f} PED")
        else:
            self.label_avg_shrapnel.config(text="Avg Shrapnel: 0.00 PED")

        self.label_items.config(text=f"Items: {self.item_value:.2f} PED")

        # Hourly Rates
        if self.start_time:
            now = datetime.now()
            duration = now - self.start_time
            seconds = duration.total_seconds()
            
            # Format duration
            hours, remainder = divmod(int(seconds), 3600)
            minutes, secs = divmod(remainder, 60)
            self.label_duration.config(text=f"Duration: {hours:02}:{minutes:02}:{secs:02}")
            
            if hours > 0 or minutes > 0:
                hours_float = seconds / 3600
                loot_hr = self.total_value / hours_float
                self.label_hourly_profit.config(text=f"Loot/Hr: {loot_hr:.2f} PED")
            else:
                self.label_hourly_profit.config(text="Loot/Hr: ...")
        else:
            self.label_duration.config(text="Duration: 00:00:00")
            self.label_hourly_profit.config(text="Loot/Hr: 0.00 PED")
            
        # Update Skills Tree
        # Clear and re-populate (simple approach for now)
        for item in self.skills_tree.get_children():
            self.skills_tree.delete(item)
        
        for skill, gain in sorted(self.skills.items(), key=lambda x: x[1], reverse=True):
            self.skills_tree.insert('', 'end', values=(skill, f"{gain:.4f}"))

    def read_log_update(self):
        if not self.is_tracking or not self.file_handle:
            return

        try:
            where = self.file_handle.tell()
            line = self.file_handle.readline()
            if not line:
                # No new line, wait and check again
                self.file_handle.seek(where)
                self.root.after(100, self.read_log_update)
                return

            # Process the line
            self.process_line(line)
            
            # Continue reading immediately in case there are multiple lines buffered
            self.root.after(1, self.read_log_update)
            
        except Exception as e:
            print(f"Error reading line: {e}")
            self.is_tracking = False
            self.status_label.config(text="Status: Error reading file")

    def process_line(self, line):
        # Extract timestamp
        ts_match = self.timestamp_pattern.match(line)
        current_ts = ts_match.group(1) if ts_match else None
        
        # Set start time if not set
        if self.start_time is None and current_ts:
             # We use current system time for duration tracking relative to when we started tracking
             # But if we are reading old logs, this might be weird. 
             # For "Live" tracking, using datetime.now() when the first event comes in is safer.
             self.start_time = datetime.now()

        # Check if it's a system message about receiving items
        if "[System] [] You received" in line:
            match = self.loot_pattern.search(line)
            if match:
                try:
                    value = float(match.group(1))
                    
                    # Check for Universal Ammo (Cost/Input)
                    if "Universal Ammo" in line:
                        # Deduct from loot value as it's no longer sellable
                        # Universal Ammo is 101% of Shrapnel value.
                        original_shrapnel_value = value / 1.01
                        self.total_value -= original_shrapnel_value
                        self.shrapnel_value -= original_shrapnel_value
                    else:
                        # It's Loot
                        self.total_value += value
                        if "Shrapnel" in line:
                            self.shrapnel_value += value
                            self.shrapnel_drop_count += 1
                        else:
                            self.item_value += value
                        
                        # Count unique loot events (kills)
                        if current_ts and current_ts != self.last_loot_time:
                            self.loot_count += 1
                            self.last_loot_time = current_ts
                        
                    self.update_display()
                except ValueError:
                    pass
        
        # Check for Skill Gains
        elif "You have gained" in line:
            # Try skill pattern
            skill_match = self.skill_pattern.search(line)
            if skill_match:
                try:
                    amount = float(skill_match.group(1))
                    skill_name = skill_match.group(2)
                    self.skills[skill_name] = self.skills.get(skill_name, 0.0) + amount
                    self.update_display()
                except ValueError:
                    pass
            else:
                # Try attribute pattern
                attr_match = self.attr_pattern.search(line)
                if attr_match:
                    try:
                        amount = float(attr_match.group(1))
                        attr_name = attr_match.group(2)
                        # Filter out "experience" if it accidentally matched here (though regex should prevent it)
                        if attr_name.lower() != "experience":
                            self.skills[attr_name] = self.skills.get(attr_name, 0.0) + amount
                            self.update_display()
                    except ValueError:
                        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = LootTrackerApp(root)
    root.mainloop()
