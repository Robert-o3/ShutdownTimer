# Shutdown Timer

A sleek, modular application for scheduling system shutdowns, built with Python and CustomTkinter.

## DOWNLOAD
[![Download Latest Release](https://img.shields.io/badge/Download-.exe-blue.svg)](https://github.com/Robert-o3/ShutdownTimer/releases/latest/download/Shutdown_Timer.exe)
[![Download Source Code](https://img.shields.io/badge/Download-Source_Code-red.svg)](https://github.com/Robert-o3/ShutdownTimer/archive/refs/heads/main.zip)

A sleek, modular application for scheduling system shutdowns, built with Python and CustomTkinter.

## Getting Started (Development)
To develop or run this project from source, you must isolate the dependencies using a virtual environment.

*   **Automated Setup:** Execute the included `setup.bat` (Windows) or `./setup.sh` (Mac/Linux) to instantly create your environment and install packages.
*   **Manual Setup:** Create an environment (`python -m venv venv`), activate it (`venv\Scripts\activate` or `source venv/bin/activate`), and install the requirements (`pip install -r requirements.txt`).
*   **Run the App:** With your environment activated, launch the application by running `python main.py` in your terminal.

## Architecture Overview
This project strictly separates sections for clean, maintainable code:
*   **`main.py`**: The application's entry point that safely connects the logic and the user interface.
*   **`frontend.py`**: Contains all CustomTkinter components, window placement, and visual styling.
*   **`backend.py`**: Handles timer math, state tracking, and local JSON configuration storage.
*   **`utils.py`**: Manages OS-level shell commands, hidden console states, and administrator privileges.

## Building the Executable (.exe)
To build the app, you need the `.ico` file. The icon name is `app_icon.ico`

Here is the complete step-by-step guide to creating the final standalone executable file:

1. **Activate your environment:** Open the terminal in VS Code and activate your venv (assuming your environment is named `venv`):
   *   On Windows: `venv\Scripts\activate`
   *   On Mac/Linux: `source venv/bin/activate`
   *(You will know it's active when you see `(venv)` appear at the start of your terminal line).*
2. **Install the Builder:** Run `pip install pyinstaller` in your terminal.
3. **Run the Final PyInstaller Build Command:** Navigate your activated venv terminal to your project folder and run this precise command:
   `pyinstaller --onefile --noconsole --icon=app_icon.ico --name "Shutdown Timer" main.py`
   *   `--onefile`: Bundles everything into one single executable file.
   *   `--noconsole`: Prevents the ugly command prompt window from popping up behind your clean GUI when the app runs.
   *   `--icon=app_icon.ico`: Sets the custom icon for your app.
   *   `--name "Shutdown Timer`: Sets the name of the app.
   *   `main.py`: The name of your entry Python script.
4. **Retrieve Your Finished Application:** Once the command completes, you will see new folders (`build`, `__pycache__`) and a `.spec` file. They are temporary and can be deleted. Your polished, standalone executable file will be waiting for you inside the `dist` folder. Double-click the file to launch your Computer Shutdown app! 

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions, bug reports, or feature requests are greatly appreciated!

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.