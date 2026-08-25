import customtkinter as ctk
import platform
import ctypes
from PIL import Image, ImageTk

# Import Utils
import utils

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class ModernShutdownApp(ctk.CTk):
    def __init__(self, backend):
        super().__init__()
        
        self.timer_backend = backend
        self.timer_id = None

        # Window Setup
        self.geometry("480x480")
        self.resizable(False, False)
        self.overrideredirect(True)

        # Taskbar Icon
        try:
            if platform.system() == "Windows":
                # Tell Windows this is a unique app, not just a generic Python script
                app_id = "custom.shutdown.timer.1"
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            
            # Try forcing the PNG icon globally via the window manager
            self.wm_iconbitmap("app_icon.ico")
            
        except Exception as e:
            print(f"Icon failed to load: {e}")

        # Bring Window to Front
        self.lift()
        self.attributes("-topmost", True)
        self.after(50, lambda: self.attributes("-topmost", False))
        self.focus_force()

        # Transparency & Rounded Corners
        if platform.system() == "Windows":
            self.wm_attributes("-transparentcolor", "#000001")
            self.configure(fg_color="#000001")
        elif platform.system() == "Darwin":
            self.wm_attributes("-transparent", True)
            self.configure(fg_color="systemTransparent")
        else:
            self.configure(fg_color="#121212")

        self.bg_frame = ctk.CTkFrame(self, fg_color="#121212", corner_radius=30)
        self.bg_frame.pack(fill="both", expand=True)

        # Custom Title Bar
        self.title_bar = ctk.CTkFrame(self.bg_frame, height=35, fg_color="transparent", corner_radius=0)
        self.title_bar.pack(fill="x", side="top", pady=(10, 0), padx=15) 

        try:
            icon_image = ctk.CTkImage(light_image=Image.open("app_icon.png"), 
                                      dark_image=Image.open("app_icon.png"), 
                                      size=(20, 20))
            self.icon_label = ctk.CTkLabel(self.title_bar, image=icon_image, text=" Shutdown Timer", 
                                           compound="left", font=("Segoe UI", 12, "bold"), text_color="#E0E0E0")
            self.icon_label.pack(side="left") 
        except Exception:
            self.icon_label = ctk.CTkLabel(self.title_bar, text="Shutdown Timer", 
                                           font=("Segoe UI", 12, "bold"), text_color="#E0E0E0")
            self.icon_label.pack(side="left")

        self.close_btn = ctk.CTkButton(self.title_bar, text="✕", width=40, height=35,
                                       fg_color="transparent", hover_color="#7a4b4b",
                                       text_color="#E0E0E0", font=("Arial", 16),
                                       command=self.destroy, corner_radius=10)
        self.close_btn.pack(side="right")

        self.min_btn = ctk.CTkButton(self.title_bar, text="—", width=40, height=35,
                                     fg_color="transparent", hover_color="#333333",
                                     text_color="#E0E0E0", font=("Arial", 16, "bold"),
                                     command=self.minimize_window, corner_radius=10)
        self.min_btn.pack(side="right", padx=(0, 5))

        # UI Panel
        self.glass_frame = ctk.CTkFrame(self.bg_frame, fg_color="transparent") 
        self.glass_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.inner_panel = ctk.CTkFrame(self.glass_frame, corner_radius=25, fg_color="#1c1c1c")
        self.inner_panel.pack(fill="both", expand=True, padx=20, pady=20)

        self.time_display = ctk.CTkLabel(self.inner_panel, text="00:00:00", font=("Arial", 56, "bold"), text_color="#E0E0E0")
        self.time_display.pack(pady=(20, 10))

        self.status_label = ctk.CTkLabel(self.inner_panel, text="", font=("Arial", 11), text_color="#c49a6c")
        self.status_label.pack(pady=5)

        self.input_container = ctk.CTkFrame(self.inner_panel, fg_color="transparent")
        self.input_container.pack(pady=15)

        self.h_input, self.h_label = self.create_spinner_column(0, "HRS", 23)
        self.m_input, self.m_label = self.create_spinner_column(1, "MIN", 59)
        self.s_input, self.s_label = self.create_spinner_column(2, "SEC", 59)

        # Fill inputs with saved config data
        saved_h, saved_m, saved_s = self.timer_backend.load_saved_time()
        self.h_input.delete(0, "end"); self.h_input.insert(0, f"{saved_h:02d}")
        self.m_input.delete(0, "end"); self.m_input.insert(0, f"{saved_m:02d}")
        self.s_input.delete(0, "end"); self.s_input.insert(0, f"{saved_s:02d}")

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

        # Bind Dragging
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
        col_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        col_frame.grid(row=0, column=col_idx, padx=10)

        up_btn = ctk.CTkButton(col_frame, text="▲", width=55, height=20, fg_color="#282828", hover_color="#383838",
                               text_color="#AAAAAA", font=("Arial", 10), corner_radius=6,
                               command=lambda: self.adjust_value(entry, 1, max_val))
        up_btn.pack(pady=(0, 3))

        entry = ctk.CTkEntry(col_frame, width=55, height=45, font=("Arial", 20, "bold"), 
                             fg_color="#282828", border_color="#333333", corner_radius=12, justify="center")
        entry.insert(0, "00")
        entry.pack()

        down_btn = ctk.CTkButton(col_frame, text="▼", width=55, height=20, fg_color="#282828", hover_color="#383838",
                                 text_color="#AAAAAA", font=("Arial", 10), corner_radius=6,
                                 command=lambda: self.adjust_value(entry, -1, max_val))
        down_btn.pack(pady=(3, 3))

        label = ctk.CTkLabel(col_frame, text=label_text, font=("Arial", 11), text_color="#888888")
        label.pack()

        return entry, label

    def adjust_value(self, entry_widget, amount, max_val):
        if entry_widget.cget("state") == "disabled": return
        try:
            current_val = int(entry_widget.get()) if entry_widget.get() else 0
        except ValueError:
            current_val = 0
            
        new_val = self.timer_backend.calculate_step(current_val, amount, max_val)
        entry_widget.delete(0, "end")
        entry_widget.insert(0, f"{new_val:02d}")

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
            
            # Save the inputs to config
            self.timer_backend.save_time(h, m, s)

            if not self.timer_backend.set_time(h, m, s):
                return

            self.start_btn.configure(state="disabled")
            self.cancel_btn.configure(state="normal")
            self.h_input.configure(state="disabled")
            self.m_input.configure(state="disabled")
            self.s_input.configure(state="disabled")
            self.status_label.configure(text="INITIATED", text_color="#c49a6c")
            
            self.update_timer()
            
        except ValueError:
            self.status_label.configure(text="INVALID INPUT", text_color="#7a4b4b")

    def update_timer(self):
        if self.timer_backend.is_running:
            self.time_display.configure(text=self.timer_backend.get_time_formatted())
            self.timer_backend.decrement()
            self.timer_id = self.after(1000, self.update_timer)
        else:
            if self.timer_backend.remaining_seconds <= 0:
                utils.execute_shutdown()

    def cancel_timer(self):
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None
            
        self.timer_backend.abort()
        self.time_display.configure(text="00:00:00")
        self.start_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.h_input.configure(state="normal")
        self.m_input.configure(state="normal")
        self.s_input.configure(state="normal")
        self.status_label.configure(text="ABORTED", text_color="#888888")