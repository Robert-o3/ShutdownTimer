import os
import platform
import sys
import ctypes

def is_admin():
    try:
        if platform.system() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except Exception:
        return False

def elevate_privileges():
    if platform.system() == "Windows":
        executable = sys.executable
        if executable.lower().endswith("python.exe"):
            executable = executable.replace("python.exe", "pythonw.exe")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", executable, " ".join(sys.argv), None, 0
        )
        sys.exit()
    else:
        print("Please run this application as root/sudo to enable shutdown capabilities.")
        sys.exit()

def hide_console():
    if platform.system() == "Windows":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def execute_shutdown():
    current_os = platform.system()
    if current_os == "Windows": 
        os.system("shutdown /s /t 0")
    elif current_os in ["Linux", "Darwin"]: 
        os.system("shutdown -h now")