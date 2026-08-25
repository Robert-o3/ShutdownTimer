import os
import json
import platform

class ShutdownTimer:
    def __init__(self):
        self.remaining_seconds = 0
        self.is_running = False
        self.config_path = self._get_config_path()

    def _get_config_path(self):
        # Determine the OS-specific path
        app_name = "ShutdownTimer"
        if platform.system() == "Windows":
            base = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA") or os.path.expanduser("~")
        elif platform.system() == "Darwin":
            base = os.path.expanduser("~/Library/Application Support")
        else:
            base = os.getenv("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
            
        config_dir = os.path.join(base, app_name)
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "config.json")

    def load_saved_time(self):
        # Loads the config values. Default is 0.
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    return data.get("h", 0), data.get("m", 0), data.get("s", 0)
            except Exception:
                pass
        return 0, 0, 0

    def save_time(self, h, m, s):
        #Save current timer
        try:
            with open(self.config_path, 'w') as f:
                json.dump({"h": h, "m": m, "s": s}, f)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def set_time(self, hours, minutes, seconds):
        self.remaining_seconds = (hours * 3600) + (minutes * 60) + seconds
        self.is_running = self.remaining_seconds > 0
        return self.is_running

    def decrement(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
        if self.remaining_seconds <= 0:
            self.is_running = False

    def get_time_formatted(self):
        m, s = divmod(self.remaining_seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def abort(self):
        self.remaining_seconds = 0
        self.is_running = False

    @staticmethod
    def calculate_step(current_val, amount, max_val):
        val = current_val + amount
        if val > max_val: return 0
        elif val < 0: return max_val
        return val