import customtkinter as ctk
import os
import platform
import sys
import ctypes
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class ModernShutdownApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.geometry("480x480")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.remaining_seconds = 0
        self.timer_id = None
        self.is_running = False

        # --- Transparency for Rounded Corners ---
        if platform.system() == "Windows":
            self.wm_attributes("-transparentcolor", "#000001")
            self.configure(fg_color="#000001")
        elif platform.system() == "Darwin": # macOS
            self.wm_attributes("-transparent", True)
            self.configure(fg_color="systemTransparent")
        else:
            self.configure(fg_color="#121212") # Linux fallback

        # Create the main rounded background frame
        self.bg_frame = ctk.CTkFrame(self, fg_color="#121212", corner_radius=30) # Increased to 30 for a rounder look
        self.bg_frame.pack(fill="both", expand=True)

        # --- Custom Title Bar ---
        self.title_bar = ctk.CTkFrame(self.bg_frame, height=35, fg_color="transparent", corner_radius=0)
        
        # Added padx=15 and increased pady to pull the title bar inwards, away from the glitching corners
        self.title_bar.pack(fill="x", side="top", pady=(10, 0), padx=15) 

        # Load and display custom icon image and text (expects 'app_icon.png' in folder)
        try:
            icon_image = ctk.CTkImage(light_image=Image.open("app_icon.png"), 
                                      dark_image=Image.open("app_icon.png"), 
                                      size=(20, 20))
            self.icon_label = ctk.CTkLabel(self.title_bar, image=icon_image, text=" Shutdown Timer", 
                                           compound="left", font=("Segoe UI", 12, "bold"), text_color="#E0E0E0")
            # Removed the extra left padding here since we added it to the title bar itself
            self.icon_label.pack(side="left") 
        except Exception:
            # Fallback text if image isn't found yet
            self.icon_label = ctk.CTkLabel(self.title_bar, text="Shutdown Timer", 
                                           font=("Segoe UI", 12, "bold"), text_color="#E0E0E0")
            self.icon_label.pack(side="left")

        # Close Button
        self.close_btn = ctk.CTkButton(self.title_bar, text="✕", width=40, height=35,
                                       fg_color="transparent", hover_color="#7a4b4b",
                                       text_color="#E0E0E0", font=("Arial", 16),
                                       command=self.destroy, corner_radius=10)
        self.close_btn.pack(side="right")

        # Minimize Button
        self.min_btn = ctk.CTkButton(self.title_bar, text="—", width=40, height=35,
                                     fg_color="transparent", hover_color="#333333",
                                     text_color="#E0E0E0", font=("Arial", 16, "bold"),
                                     command=self.minimize_window, corner_radius=10)
        self.min_btn.pack(side="right", padx=(0, 5))

        # --- Main UI Panel ---
        self.glass_frame = ctk.CTkFrame(self.bg_frame, fg_color="transparent") 
        self.glass_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.inner_panel = ctk.CTkFrame(self.glass_frame, corner_radius=25, fg_color="#1c1c1c")
        self.inner_panel.pack(fill="both", expand=True, padx=20, pady=20)

        # Main Timer Display
        self.time_display = ctk.CTkLabel(self.inner_panel, text="00:00:00", font=("Arial", 56, "bold"), text_color="#E0E0E0")
        self.time_display.pack(pady=(20, 10))

        # Status Label
        self.status_label = ctk.CTkLabel(self.inner_panel, text="", font=("Arial", 11), text_color="#c49a6c")
        self.status_label.pack(pady=5)

        # Inputs Section with Step-Up/Step-Down Buttons
        self.input_container = ctk.CTkFrame(self.inner_panel, fg_color="transparent")
        self.input_container.pack(pady=15)

        # Create input columns with arrows
        self.h_input, self.h_label = self.create_spinner_column(0, "HRS", 23)
        self.m_input, self.m_label = self.create_spinner_column(1, "MIN", 59)
        self.s_input, self.s_label = self.create_spinner_column(2, "SEC", 59)

        # Buttons Section
        self.button_container = ctk.CTkFrame(self.inner_panel, fg_color="transparent")
        self.button_container.pack(pady=20)

        self.start_btn = ctk.CTkButton(self.button_container, text="Shutdown", command=self.start_timer, 
                                        font=("Arial", 14, "bold"), height=45, width=150, corner_radius=20,
                                        fg_color="#4e7355", hover_color="#5a8763", text_color="#FFFFFF")
        self.start_btn.grid(row=0, column=0, padx=15)

        self.cancel_btn = ctk.CTkButton(self.button_container, text="Abort", command=self.cancel_timer, state="disabled",
                                        font=("Arial", 14, "bold"), height=45, width=150, corner_radius=20,
                                        fg_color="#7a4b4b", hover_color="#915858", text_color="#FFFFFF", text_color_disabled="#666666")
        self.cancel_btn.grid(row=0, column=1, padx=15)

        # --- Bind Dragging to Background elements ---
        draggable_widgets = [
            self, self.bg_frame, self.title_bar, self.icon_label, self.glass_frame, 
            self.inner_panel, self.time_display, self.status_label, 
            self.input_container, self.h_label, self.m_label, self.s_label, 
            self.button_container
        ]
        
        for widget in draggable_widgets:
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)

        self.bind("<Map>", self.restore_window)

    def create_spinner_column(self, col_idx, label_text, max_val):
        """Helper to create an entry box stacked between an Up and Down arrow button"""
        col_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        col_frame.grid(row=0, column=col_idx, padx=10)

        # Up Arrow
        up_btn = ctk.CTkButton(col_frame, text="▲", width=55, height=20, fg_color="#282828", hover_color="#383838",
                               text_color="#AAAAAA", font=("Arial", 10), corner_radius=6,
                               command=lambda: self.adjust_value(entry, 1, max_val))
        up_btn.pack(pady=(0, 3))

        # Number Entry
        entry = ctk.CTkEntry(col_frame, width=55, height=45, font=("Arial", 20, "bold"), 
                             fg_color="#282828", border_color="#333333", corner_radius=12, justify="center")
        entry.insert(0, "00")
        entry.pack()

        # Down Arrow
        down_btn = ctk.CTkButton(col_frame, text="▼", width=55, height=20, fg_color="#282828", hover_color="#383838",
                                 text_color="#AAAAAA", font=("Arial", 10), corner_radius=6,
                                 command=lambda: self.adjust_value(entry, -1, max_val))
        down_btn.pack(pady=(3, 3))

        # Label (HRS / MIN / SEC)
        label = ctk.CTkLabel(col_frame, text=label_text, font=("Arial", 11), text_color="#888888")
        label.pack()

        return entry, label

    def adjust_value(self, entry_widget, amount, max_val):
        if entry_widget.cget("state") == "disabled":
            return
        try:
            val = int(entry_widget.get()) if entry_widget.get() else 0
        except ValueError:
            val = 0
        
        val += amount
        # Wrap around or clamp logic
        if val > max_val:
            val = 0
        elif val < 0:
            val = max_val

        entry_widget.delete(0, "end")
        entry_widget.insert(0, f"{val:02d}")

    def start_move(self, event):
        self.last_click_x = event.x
        self.last_click_y = event.y

    def do_move(self, event):
        x = self.winfo_x() + event.x - self.last_click_x
        y = self.winfo_y() + event.y - self.last_click_y
        self.geometry(f"+{x}+{y}")

    def minimize_window(self):
        self.overrideredirect(False)
        self.iconify()

    def restore_window(self, event):
        if self.state() == "normal":
            self.overrideredirect(True)

    def start_timer(self):
        try:
            h = int(self.h_input.get()) if self.h_input.get() else 0
            m = int(self.m_input.get()) if self.m_input.get() else 0
            s = int(self.s_input.get()) if self.s_input.get() else 0
            
            self.remaining_seconds = (h * 3600) + (m * 60) + s
            if self.remaining_seconds <= 0: return

            self.start_btn.configure(state="disabled")
            self.cancel_btn.configure(state="normal")
            self.h_input.configure(state="disabled")
            self.m_input.configure(state="disabled")
            self.s_input.configure(state="disabled")
            self.status_label.configure(text="INITIATED", text_color="#c49a6c")
            
            self.is_running = True
            self.update_timer()
            
        except ValueError:
            self.status_label.configure(text="INVALID INPUT", text_color="#7a4b4b")

    def update_timer(self):
        if self.remaining_seconds > 0:
            m, s = divmod(self.remaining_seconds, 60)
            h, m = divmod(m, 60)
            self.time_display.configure(text=f"{h:02d}:{m:02d}:{s:02d}")
            self.remaining_seconds -= 1
            self.timer_id = self.after(1000, self.update_timer)
        else:
            self.is_running = False
            self.execute_shutdown()

    def cancel_timer(self):
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None
            
        self.is_running = False
        self.time_display.configure(text="00:00:00")
        self.start_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.h_input.configure(state="normal")
        self.m_input.configure(state="normal")
        self.s_input.configure(state="normal")
        self.status_label.configure(text="ABORTED", text_color="#888888")

    def execute_shutdown(self):
        current_os = platform.system()
        if current_os == "Windows": os.system("shutdown /s /t 0")
        elif current_os in ["Linux", "Darwin"]: os.system("shutdown -h now")

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        # Windows check
        if platform.system() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin()
        # Linux/macOS check
        else:
            return os.geteuid() == 0
    except Exception:
        return False

if __name__ == "__main__":
    if not is_admin():
        # If not admin, attempt to relaunch with elevation
        if platform.system() == "Windows":
            # Ensure we use pythonw.exe to prevent the console from spawning on elevation
            executable = sys.executable
            if executable.lower().endswith("python.exe"):
                executable = executable.replace("python.exe", "pythonw.exe")
                
            # Trigger the Windows UAC prompt (last parameter '0' requests it to run hidden)
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", executable, " ".join(sys.argv), None, 0
            )
            sys.exit()
        else:
            print("Please run this application as root/sudo to enable shutdown capabilities.")
            sys.exit()
            
    # Force-hide the console window programmatically just in case it still flashes
    if platform.system() == "Windows":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
    # If we are admin, run the app normally
    app = ModernShutdownApp()
    app.mainloop()