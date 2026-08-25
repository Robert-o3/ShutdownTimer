import customtkinter as ctk
import os
import platform

# Initialize CustomTkinter (gives us the modern look)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")  # Using default blue theme

class NeuralShutdownInterface(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("NEURAL SHUTDOWN INTERFACE")
        self.geometry("450x380")
        self.resizable(False, False)
        
        # Configure a subtle geometric grid background
        self.bg_frame = ctk.CTkFrame(self, fg_color="#0d0d0d")
        self.bg_frame.pack(fill="both", expand=True)

        self.remaining_seconds = 0
        self.timer_id = None
        self.is_running = False

        # --- UI Design Elements ---
        
        # 1. Main Header
        self.header_label = ctk.CTkLabel(self.bg_frame, 
                                        text="NEURAL SHUTDOWN INTERFACE", 
                                        font=("Orbitron", 16, "bold"), # Modern angular font
                                        text_color="#888888")
        self.header_label.pack(pady=20)

        # 2. Main Timer Display
        self.time_display = ctk.CTkLabel(self.bg_frame, 
                                        text="00:00:00", 
                                        font=("Orbitron", 54, "bold"), # Main glowing number look
                                        text_color="#00FFFF")         # Cyan
        self.time_display.pack(pady=10)

        # 3. Status Label (Sequence Initiated / Cancelled)
        self.status_label = ctk.CTkLabel(self.bg_frame, text="", font=("Orbitron", 10), text_color="#FF00FF") # Magenta accent
        self.status_label.pack(pady=5)

        # 4. Inputs Section
        self.input_container = ctk.CTkFrame(self.bg_frame, fg_color="transparent")
        self.input_container.pack(pady=15)

        entry_params = {"width": 60, "height": 45, "font": ("Orbitron", 22, "bold"), "fg_color": "#1A1A1A", "border_color": "#2A2A2A", "justify": "center"}
        label_params = {"font": ("Orbitron", 11), "text_color": "#888888"}

        # Custom inputs with the labels beneath
        input_w = ctk.CTkFrame(self.input_container, fg_color="transparent")
        input_w.grid(row=0, column=0, padx=10)
        self.h_input = ctk.CTkEntry(input_w, placeholder_text="00", **entry_params)
        self.h_input.pack()
        ctk.CTkLabel(input_w, text="H", **label_params).pack()

        input_w = ctk.CTkFrame(self.input_container, fg_color="transparent")
        input_w.grid(row=0, column=1, padx=10)
        self.m_input = ctk.CTkEntry(input_w, placeholder_text="00", **entry_params)
        self.m_input.pack()
        ctk.CTkLabel(input_w, text="M", **label_params).pack()

        input_w = ctk.CTkFrame(self.input_container, fg_color="transparent")
        input_w.grid(row=0, column=2, padx=10)
        self.s_input = ctk.CTkEntry(input_w, placeholder_text="00", **entry_params)
        self.s_input.pack()
        ctk.CTkLabel(input_w, text="S", **label_params).pack()

        # 5. Buttons Section
        self.button_container = ctk.CTkFrame(self.bg_frame, fg_color="transparent")
        self.button_container.pack(pady=20)

        # Style like the generated image (Initiate, glowing blue/green)
        self.start_btn = ctk.CTkButton(self.button_container, 
                                        text="INITIATE SEQUENCE", 
                                        command=self.start_timer, 
                                        font=("Orbitron", 13, "bold"),
                                        height=40,
                                        fg_color="#008080",      # Deeper blue-green
                                        hover_color="#00AAAA",   # Brighter hover
                                        border_width=2,
                                        border_color="#00FFFF")
        self.start_btn.grid(row=0, column=0, padx=15)

        # Style like the generated image (Abort, deep red)
        self.cancel_btn = ctk.CTkButton(self.button_container, 
                                        text="ABORT SEQUENCE", 
                                        command=self.cancel_timer, 
                                        state="disabled",
                                        font=("Orbitron", 13, "bold"),
                                        height=40,
                                        fg_color="#330000",      # Dark, almost burgundy
                                        hover_color="#AA0000",   # Brighter red hover
                                        border_width=2,
                                        border_color="#FF0000",  # Red border
                                        text_color_disabled="#666666")
        self.cancel_btn.grid(row=0, column=1, padx=15)

    def start_timer(self):
        try:
            h = int(self.h_input.get()) if self.h_input.get() else 0
            m = int(self.m_input.get()) if self.m_input.get() else 0
            s = int(self.s_input.get()) if self.s_input.get() else 0
            
            self.remaining_seconds = (h * 3600) + (m * 60) + s
            
            if self.remaining_seconds <= 0: return

            # UI Update
            self.start_btn.configure(state="disabled")
            self.cancel_btn.configure(state="normal")
            self.h_input.configure(state="disabled")
            self.m_input.configure(state="disabled")
            self.s_input.configure(state="disabled")
            self.status_label.configure(text="SEQUENCE INITIATED", text_color="#FF00FF") # Magenta status
            
            self.is_running = True
            self.update_timer()
            
        except ValueError:
            self.status_label.configure(text="ERROR: INVALID INPUT", text_color="red")

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
        self.status_label.configure(text="SEQUENCE ABORTED", text_color="#AAAAAA")

    def execute_shutdown(self):
        current_os = platform.system()
        if current_os == "Windows": os.system("shutdown /s /t 0")
        elif current_os in ["Linux", "Darwin"]: os.system("shutdown -h now")

if __name__ == "__main__":
    app = NeuralShutdownInterface()
    app.mainloop()