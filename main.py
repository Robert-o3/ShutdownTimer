import customtkinter as ctk
import os
import platform

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class ModernShutdownApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.geometry("480x450")
        self.resizable(False, False)
        self.configure(fg_color="#0d0d0d") 

        # 1. REMOVE STANDARD OS WINDOW BAR & BORDERS
        self.overrideredirect(True)

        self.remaining_seconds = 0
        self.timer_id = None
        self.is_running = False

        # --- Custom Title Bar ---
        self.title_bar = ctk.CTkFrame(self, height=35, fg_color="#0d0d0d", corner_radius=0)
        self.title_bar.pack(fill="x", side="top")

        # Bind dragging events to the custom title bar
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        # Title text inside the custom bar
        self.title_label = ctk.CTkLabel(self.title_bar, text="SHUTDOWN", font=("Arial", 12, "bold"), text_color="#888888")
        self.title_label.pack(side="left", padx=15)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)

        # Close Button (Red X)
        self.close_btn = ctk.CTkButton(self.title_bar, text="✕", width=40, height=35,
                                       fg_color="transparent", hover_color="#990000", # Red hover
                                       text_color="#FFFFFF", font=("Arial", 16),
                                       command=self.destroy, corner_radius=0)
        self.close_btn.pack(side="right")

        # Minimize Button (—)
        self.min_btn = ctk.CTkButton(self.title_bar, text="—", width=40, height=35,
                                     fg_color="transparent", hover_color="#333333",
                                     text_color="#FFFFFF", font=("Arial", 16, "bold"),
                                     command=self.minimize_window, corner_radius=0)
        self.min_btn.pack(side="right")

        # --- Main UI Panel ---
        self.glass_frame = ctk.CTkFrame(self, fg_color="transparent", border_width=1, border_color="#2A2A2A")
        self.glass_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.inner_panel = ctk.CTkFrame(self.glass_frame, corner_radius=25, fg_color="#1a1a1a")
        self.inner_panel.pack(fill="both", expand=True, padx=20, pady=20)

        # Main Timer Display
        self.time_display = ctk.CTkLabel(self.inner_panel, text="00:00:00", font=("Arial", 56, "bold"), text_color="#FFFFFF")
        self.time_display.pack(pady=(20, 10))

        # Status Label
        self.status_label = ctk.CTkLabel(self.inner_panel, text="", font=("Arial", 11), text_color="#CC7A00")
        self.status_label.pack(pady=5)

        # Inputs Section
        self.input_container = ctk.CTkFrame(self.inner_panel, fg_color="transparent")
        self.input_container.pack(pady=15)

        entry_params = {"width": 65, "height": 50, "font": ("Arial", 24, "bold"), "fg_color": "#2A2A2A", "border_color": "#3A3A3A", "corner_radius": 15, "justify": "center"}
        label_params = {"font": ("Arial", 11), "text_color": "#AAAAAA"}

        # H / M / S Inputs
        input_w = ctk.CTkFrame(self.input_container, fg_color="transparent")
        input_w.grid(row=0, column=0, padx=12)
        self.h_input = ctk.CTkEntry(input_w, placeholder_text="00", **entry_params)
        self.h_input.pack()
        ctk.CTkLabel(input_w, text="HRS", **label_params).pack()

        input_w = ctk.CTkFrame(self.input_container, fg_color="transparent")
        input_w.grid(row=0, column=1, padx=12)
        self.m_input = ctk.CTkEntry(input_w, placeholder_text="00", **entry_params)
        self.m_input.pack()
        ctk.CTkLabel(input_w, text="MIN", **label_params).pack()

        input_w = ctk.CTkFrame(self.input_container, fg_color="transparent")
        input_w.grid(row=0, column=2, padx=12)
        self.s_input = ctk.CTkEntry(input_w, placeholder_text="00", **entry_params)
        self.s_input.pack()
        ctk.CTkLabel(input_w, text="SEC", **label_params).pack()

        # Buttons Section
        self.button_container = ctk.CTkFrame(self.inner_panel, fg_color="transparent")
        self.button_container.pack(pady=20)

        self.start_btn = ctk.CTkButton(self.button_container, text="Shutdown", command=self.start_timer, 
                                        font=("Arial", 14, "bold"), height=45, width=150, corner_radius=20,
                                        fg_color="#154d24", hover_color="#1f6932", text_color="#FFFFFF")
        self.start_btn.grid(row=0, column=0, padx=15)

        self.cancel_btn = ctk.CTkButton(self.button_container, text="Abort", command=self.cancel_timer, state="disabled",
                                        font=("Arial", 14, "bold"), height=45, width=150, corner_radius=20,
                                        fg_color="#511414", hover_color="#6e1b1b", text_color="#FFFFFF", text_color_disabled="#666666")
        self.cancel_btn.grid(row=0, column=1, padx=15)

        # Restore borderless state when app is un-minimized from taskbar
        self.bind("<Map>", self.restore_window)

    # --- Window Dragging Logic ---
    def start_move(self, event):
        self.last_click_x = event.x
        self.last_click_y = event.y

    def do_move(self, event):
        x = self.winfo_x() + event.x - self.last_click_x
        y = self.winfo_y() + event.y - self.last_click_y
        self.geometry(f"+{x}+{y}")

    # --- Minimize Logic for Borderless Windows ---
    def minimize_window(self):
        # A borderless window normally disappears completely when minimized.
        # We briefly restore standard borders so the OS puts it in the taskbar correctly.
        self.overrideredirect(False)
        self.iconify()

    def restore_window(self, event):
        # When clicked in the taskbar to restore, remove borders again
        if self.state() == "normal":
            self.overrideredirect(True)

    # --- Timer Logic ---
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
            self.status_label.configure(text="INITIATED", text_color="#CC7A00")
            
            self.is_running = True
            self.update_timer()
            
        except ValueError:
            self.status_label.configure(text="INVALID INPUT", text_color="#990000")

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
        self.status_label.configure(text="ABORTED", text_color="#AAAAAA")

    def execute_shutdown(self):
        current_os = platform.system()
        if current_os == "Windows": os.system("shutdown /s /t 0")
        elif current_os in ["Linux", "Darwin"]: os.system("shutdown -h now")

if __name__ == "__main__":
    app = ModernShutdownApp()
    app.mainloop()