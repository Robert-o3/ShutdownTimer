import utils
from backend import ShutdownTimer
from frontend import ModernShutdownApp

if __name__ == "__main__":
    # Checks and prep
    if not utils.is_admin():
        utils.elevate_privileges()
        
    utils.hide_console()
    
    # Init. Data & State
    timer_backend = ShutdownTimer()
    
    # Init. UI
    app = ModernShutdownApp(timer_backend)
    
    # Run app.
    app.mainloop()