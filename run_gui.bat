@echo off
REM Unsafe File Scanner GUI Launcher
REM This batch file launches the GUI application

echo Starting Unsafe File Scanner GUI...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Run the GUI
python run_gui.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit.
    pause
)


