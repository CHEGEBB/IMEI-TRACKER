import requests
import time
import webbrowser
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import threading
from datetime import datetime
import re
import json
from pathlib import Path
from tkinter import font
import os

class FontManager:
    @staticmethod
    def load_rubik_font():
        # Create fonts directory if it doesn't exist
        os.makedirs("fonts", exist_ok=True)
        
        # Define font files to check/download
        font_files = {
            "Rubik-Regular.ttf": "https://github.com/googlefonts/rubik/raw/main/fonts/ttf/Rubik-Regular.ttf",
            "Rubik-Bold.ttf": "https://github.com/googlefonts/rubik/raw/main/fonts/ttf/Rubik-Bold.ttf",
            "Rubik-Medium.ttf": "https://github.com/googlefonts/rubik/raw/main/fonts/ttf/Rubik-Medium.ttf"
        }
        
        # Download missing font files
        for font_file, url in font_files.items():
            font_path = f"fonts/{font_file}"
            if not os.path.exists(font_path):
                try:
                    response = requests.get(url)
                    with open(font_path, 'wb') as f:
                        f.write(response.content)
                except Exception as e:
                    print(f"Error downloading font: {e}")
                    return False
        
        # Load fonts into Tkinter
        for font_file in font_files.keys():
            font_path = f"fonts/{font_file}"
            try:
                font.families()  # Initialize font system
                font.Font(file=font_path)
            except Exception as e:
                print(f"Error loading font: {e}")
                return False
        
        return True

class CustomFont:
    REGULAR = "Rubik"
    MEDIUM = "Rubik Medium"
    BOLD = "Rubik Bold"
    
    # Font sizes
    H1 = 24
    H2 = 18
    H3 = 16
    BODY = 12
    SMALL = 10

class ThemeColors:
    PRIMARY = '#2C3E50'
    SECONDARY = '#34495E'
    ACCENT = '#3498DB'
    SUCCESS = '#27AE60'
    ERROR = '#E74C3C'
    WARNING = '#F39C12'
    TEXT_LIGHT = '#ECF0F1'
    TEXT_DARK = '#2C3E50'
    GRAY = '#BDC3C7'

class LoginWindow:
    def __init__(self, on_login_success):
        self.window = Tk()
        self.window.title("🔐 Secure Login")
        self.window.geometry("400x600")
        self.window.configure(bg=ThemeColors.PRIMARY)
        
        self.on_login_success = on_login_success
        
        # Header
        self.header = Label(
            self.window,
            text="🌟 Welcome to Device Tracker Pro",
            font=(CustomFont.BOLD, CustomFont.H2),
            bg=ThemeColors.PRIMARY,
            fg=ThemeColors.TEXT_LIGHT
        )
        self.header.pack(pady=20)
        
        # Login frame
        self.login_frame = Frame(self.window, bg=ThemeColors.SECONDARY, padx=20, pady=20)
        self.login_frame.pack(fill=X, padx=20)
        
        # Email
        Label(
            self.login_frame,
            text="📧 Email",
            bg=ThemeColors.SECONDARY,
            fg=ThemeColors.TEXT_LIGHT,
            font=(CustomFont.MEDIUM, CustomFont.BODY)
        ).pack(pady=5)
        
        self.email_entry = Entry(
            self.login_frame,
            font=(CustomFont.REGULAR, CustomFont.BODY),
            bg=ThemeColors.TEXT_LIGHT
        )
        self.email_entry.pack(fill=X, pady=5)
        
        # Password
        Label(
            self.login_frame,
            text="🔑 Password",
            bg=ThemeColors.SECONDARY,
            fg=ThemeColors.TEXT_LIGHT,
            font=(CustomFont.MEDIUM, CustomFont.BODY)
        ).pack(pady=5)
        
        self.password_entry = Entry(
            self.login_frame,
            font=(CustomFont.REGULAR, CustomFont.BODY),
            bg=ThemeColors.TEXT_LIGHT,
            show="•"
        )
        self.password_entry.pack(fill=X, pady=5)
        
        # Remember me
        self.remember_var = BooleanVar()
        Checkbutton(
            self.login_frame,
            text="Remember me",
            variable=self.remember_var,
            bg=ThemeColors.SECONDARY,
            fg=ThemeColors.TEXT_LIGHT,
            selectcolor=ThemeColors.PRIMARY,
            font=(CustomFont.REGULAR, CustomFont.SMALL)
        ).pack(pady=10)
        
        # Login button with hover effect
        self.login_button = Button(
            self.login_frame,
            text="🚀 Login",
            command=self.login,
            bg=ThemeColors.SUCCESS,
            fg=ThemeColors.TEXT_LIGHT,
            font=(CustomFont.BOLD, CustomFont.BODY),
            width=15,
            height=2,
            relief=FLAT,
            cursor="hand2"
        )
        self.login_button.pack(pady=10)
        
        # Add hover effect
        self.login_button.bind("<Enter>", lambda e: self.login_button.configure(bg=ThemeColors.ACCENT))
        self.login_button.bind("<Leave>", lambda e: self.login_button.configure(bg=ThemeColors.SUCCESS))
        
        # Register link
        self.register_button = Button(
            self.login_frame,
            text="📝 New User? Register Here",
            command=self.show_register,
            bg=ThemeColors.SECONDARY,
            fg=ThemeColors.ACCENT,
            font=(CustomFont.REGULAR, CustomFont.SMALL, "underline"),
            bd=0,
            relief=FLAT,
            cursor="hand2"
        )
        self.register_button.pack(pady=5)
        
        # Status label
        self.status_label = Label(
            self.login_frame,
            text="",
            bg=ThemeColors.SECONDARY,
            fg=ThemeColors.ERROR,
            font=(CustomFont.REGULAR, CustomFont.SMALL)
        )
        self.status_label.pack(pady=5)
        
        # Load saved credentials if any
        self.load_saved_credentials()
        
        # Status label
        self.status_label = Label(
            self.login_frame,
            text="",
            bg='#34495E',
            fg='#E74C3C',
            font=("Rubik", 10)
        )
        self.status_label.pack(pady=5)
        
        # Load saved credentials if any
        self.load_saved_credentials()
        
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
        
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            self.status_label.config(text="❌ Please fill in all fields")
            return
            
        if not self.validate_email(email):
            self.status_label.config(text="❌ Invalid email format")
            return
            
        # Simulate login verification
        self.login_button.config(state=DISABLED, text="🔄 Logging in...")
        self.window.after(1500, lambda: self.process_login(email, password))
        
    def process_login(self, email, password):
        # Save credentials if remember me is checked
        if self.remember_var.get():
            self.save_credentials(email, password)
            
        self.window.destroy()
        self.on_login_success(email)
        
    def show_register(self):
        RegisterWindow(self.window)
        
    def save_credentials(self, email, password):
        data = {'email': email, 'password': password}
        Path('credentials.json').write_text(json.dumps(data))
        
    def load_saved_credentials(self):
        try:
            if Path('credentials.json').exists():
                data = json.loads(Path('credentials.json').read_text())
                self.email_entry.insert(0, data.get('email', ''))
                self.password_entry.insert(0, data.get('password', ''))
                self.remember_var.set(True)
        except:
            pass
            
    def run(self):
        self.window.mainloop()

class RegisterWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("📝 Register New Account")
        self.window.geometry("400x500")
        self.window.configure(bg='#2C3E50')
        
        # Register frame
        self.register_frame = Frame(self.window, bg='#34495E', padx=20, pady=20)
        self.register_frame.pack(fill=X, padx=20, pady=20)
        
        # Fields
        fields = [
            ("👤 Full Name", "name"),
            ("📧 Email", "email"),
            ("🔑 Password", "password"),
            ("🔄 Confirm Password", "confirm_password")
        ]
        
        self.entries = {}
        for label_text, key in fields:
            Label(
                self.register_frame,
                text=label_text,
                bg='#34495E',
                fg='white',
                font=("Rubik", 12)
            ).pack(pady=5)
            
            entry = Entry(
                self.register_frame,
                font=("Rubik", 12),
                bg='#ECF0F1'
            )
            if 'password' in key:
                entry.config(show="•")
            entry.pack(fill=X, pady=5)
            self.entries[key] = entry
            
        # Register button
        Button(
            self.register_frame,
            text="📝 Register",
            command=self.register,
            bg='#27AE60',
            fg='white',
            font=("Rubik", 12, "bold"),
            width=15,
            height=2,
            relief=FLAT
        ).pack(pady=20)
        
        # Status label
        self.status_label = Label(
            self.register_frame,
            text="",
            bg='#34495E',
            fg='#E74C3C',
            font=("Rubik", 10)
        )
        self.status_label.pack(pady=5)
        
    def register(self):
        # Validate fields
        if not all(entry.get() for entry in self.entries.values()):
            self.status_label.config(text="❌ Please fill in all fields")
            return
            
        if self.entries['password'].get() != self.entries['confirm_password'].get():
            self.status_label.config(text="❌ Passwords don't match")
            return
            
        # Simulate registration success
        self.status_label.config(text="✅ Registration successful!", fg='#27AE60')
        self.window.after(1500, self.window.destroy)

class AnimatedLabel(Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33F5']
        self.current_color = 0
        
    def animate(self):
        self.configure(fg=self.colors[self.current_color])
        self.current_color = (self.current_color + 1) % len(self.colors)
        self.after(1000, self.animate)

class LoadingBar:
    def __init__(self, master, width=300):
        self.progress = ttk.Progressbar(
            master, 
            orient="horizontal",
            length=width,
            mode="determinate"
        )
        self.progress.pack(pady=10)
        self.progress.pack_forget()
        
    def start(self):
        self.progress.pack(pady=10)
        self.progress["value"] = 0
        
    def update(self, value):
        self.progress["value"] = value
        
    def hide(self):
        self.progress.pack_forget()

class DeviceTracker:
    def __init__(self, user_email):
        self.root = Tk()
        self.root.title("📱 Advanced Device Tracker Pro")
        self.root.geometry("600x800")
        self.root.configure(bg='#2C3E50')
        
        # User info
        self.user_email = user_email
        
        # Custom styles
        style = ttk.Style()
        style.configure("TButton", padding=10, font=('Helvetica', 10))
        style.configure("TProgressbar", thickness=20, background='#27AE60')
        
        # Header with user info
        self.header_frame = Frame(self.root, bg='#2C3E50')
        self.header_frame.pack(fill=X, pady=10)
        
        self.header = AnimatedLabel(
            self.header_frame,
            text="📱 Advanced Device Tracker Pro",
            font=("Rubik", 24, "bold"),
            bg='#2C3E50',
            fg='white'
        )
        self.header.pack(pady=10)
        self.header.animate()
        
        # User info
        Label(
            self.header_frame,
            text=f"👤 Logged in as: {user_email}",
            font=("Rubik", 10),
            bg='#2C3E50',
            fg='#BDC3C7'
        ).pack()
        
         # Time display
        self.time_label = Label(
            self.root,
            font=("Rubik", 12),
            bg='#2C3E50',
            fg='#ECF0F1'
        )
        self.time_label.pack()
        self.update_time()
        
        # Main frame
        self.main_frame = Frame(self.root, bg='#34495E', padx=20, pady=20)
        self.main_frame.pack(fill=X, padx=20)
        
        # Device selection
        self.device_var = StringVar(self.root)
        self.device_var.set("Android")
        
        device_frame = LabelFrame(
            self.main_frame,
            text="Select Device Type",
            bg='#34495E',
            fg='white',
            font=("Helvetica", 12)
        )
        device_frame.pack(fill=X, pady=10)
        
        for device in ["Android", "iPhone"]:
            Radiobutton(
                device_frame,
                text=device,
                variable=self.device_var,
                value=device,
                bg='#34495E',
                fg='white',
                selectcolor='#2C3E50',
                command=self.update_ui
            ).pack(side=LEFT, padx=10)
        
        # Input frames
        self.android_frame = Frame(self.main_frame, bg='#34495E')
        self.iphone_frame = Frame(self.main_frame, bg='#34495E')
        
        # Android inputs
        Label(
            self.android_frame,
            text="IMEI Number:",
            bg='#34495E',
            fg='white',
            font=("Rubik", 12)
        ).pack(pady=5)
        self.imei_entry = Entry(
            self.android_frame,
            font=("Rubik", 12),
            bg='#ECF0F1'
        )
        self.imei_entry.pack(fill=X, pady=5)
        
        # iPhone inputs
        Label(
            self.iphone_frame,
            text="Apple ID:",
            bg='#34495E',
            fg='white',
            font=("Rubik", 12)
        ).pack(pady=5)
        self.apple_id_entry = Entry(
            self.iphone_frame,
            font=("Rubik", 12),
            bg='#ECF0F1'
        )
        self.apple_id_entry.pack(fill=X, pady=5)
        
        # Loading bar
        self.loading_bar = LoadingBar(self.main_frame)
        
        # Status display
        self.status_frame = LabelFrame(
            self.root,
            text="Status Log",
            bg='#34495E',
            fg='white',
            font=("Rubik", 12)
        )
        self.status_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        self.status_display = Text(
            self.status_frame,
            height=15,
            width=50,
            bg='#ECF0F1',
            fg='#2C3E50',
            font=("Courier", 10),
            state=DISABLED
        )
        self.status_display.pack(padx=10, pady=10, fill=BOTH, expand=True)
        
        # Buttons
        self.button_frame = Frame(self.root, bg='#2C3E50')
        self.button_frame.pack(pady=20)
        
        buttons = [
            ("Track Device", self.track_device, '#27AE60'),
            ("Clear Log", self.clear_status, '#E74C3C')
        ]
        
        for text, command, color in buttons:
            Button(
                self.button_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=("Rubik", 12, "bold"),
                width=15,
                height=2,
                relief=FLAT
            ).pack(side=LEFT, padx=10)
        
        self.update_ui()
        
    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def update_ui(self):
        frames = {
            "Android": (self.android_frame, self.iphone_frame),
            "iPhone": (self.iphone_frame, self.android_frame)
        }
        show_frame, hide_frame = frames[self.device_var.get()]
        hide_frame.pack_forget()
        show_frame.pack(fill=X, pady=10)
        
    def log_status(self, message, level="info"):
        colors = {
            "info": "#2C3E50",
            "success": "#27AE60",
            "error": "#E74C3C",
            "warning": "#F39C12"
        }
        
        self.status_display.config(state=NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_display.insert(END, f"[{timestamp}] ", "timestamp")
        self.status_display.insert(END, f"{message}\n", level)
        self.status_display.tag_config("timestamp", foreground="#7F8C8D")
        self.status_display.tag_config(level, foreground=colors.get(level, "#2C3E50"))
        self.status_display.see(END)
        self.status_display.config(state=DISABLED)
        
    def authenticate(self, credentials):
        time.sleep(1)  # Simulate authentication
        return True
        
    def request_location(self, device_id):
        time.sleep(2)  # Simulate location request
        return "37.7749,-122.4194"  # Sample coordinates
        
    def simulate_tracking_progress(self):
        steps = [
            ("Initializing tracking system...", 10),
            ("Connecting to secure servers...", 30),
            ("Authenticating credentials...", 50),
            ("Requesting device location...", 70),
            ("Processing location data...", 90),
            ("Finalizing results...", 100)
        ]
        
        for message, progress in steps:
            self.log_status(message)
            self.loading_bar.update(progress)
            time.sleep(0.5)
            
    def track_device(self):
        def tracking_thread():
            self.loading_bar.start()
            device_type = self.device_var.get()
            
            try:
                if device_type == "Android":
                    imei = self.imei_entry.get()
                    if not imei:
                        self.log_status("Please enter IMEI number", "error")
                        return
                    
                    self.log_status(f"Tracking Android device: {imei}")
                    self.simulate_tracking_progress()
                    
                    location = self.request_location(imei)
                    if location:
                        url = f"https://www.google.com/android/find?u=0&hl=en&source=android-browser&q={location}"
                        webbrowser.open(url)
                        self.log_status("Location found! Opening map...", "success")
                    
                else:  # iPhone
                    apple_id = self.apple_id_entry.get()
                    if not apple_id:
                        self.log_status("Please enter Apple ID", "error")
                        return
                    
                    self.log_status(f"Tracking iPhone device: {apple_id}")
                    self.simulate_tracking_progress()
                    self.log_status("iPhone tracking completed", "success")
                    
            except Exception as e:
                self.log_status(f"Error: {str(e)}", "error")
            finally:
                self.loading_bar.hide()
        
        threading.Thread(target=tracking_thread).start()
        
    def clear_status(self):
        self.status_display.config(state=NORMAL)
        self.status_display.delete(1.0, END)
        self.status_display.config(state=DISABLED)
        self.log_status("Status log cleared", "info")
        
    def run(self):
        self.root.mainloop()
        
def main():
    def start_main_app(user_email):
        app = DeviceTracker(user_email)
        app.run()
    
    login_window = LoginWindow(start_main_app)
    login_window.run()

if __name__ == "__main__":
    main()