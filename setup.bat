@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo Setup complete! 
echo To run the app, open your terminal here and type: venv\Scripts\python main.py
pause