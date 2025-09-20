@echo off
REM Installation script for Unsafe File Scanner (Windows)

echo 🔒 Installing Unsafe File Scanner...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not installed.
    echo Please install Python 3.8 or higher and try again.
    pause
    exit /b 1
)

echo ✅ Python detected

REM Install the package
echo 📦 Installing package...
pip install -e .

REM Create desktop shortcut
echo 🖥️ Creating desktop shortcut...
set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\Unsafe File Scanner.lnk"

REM Create a batch file to run the GUI
echo @echo off > "unsafe-file-scanner-gui.bat"
echo python -m unsafe_file_scanner_gui >> "unsafe-file-scanner-gui.bat"

echo.
echo 🎉 Installation completed successfully!
echo.
echo Usage:
echo   Command Line: unsafe-file-scanner
echo   GUI:          unsafe-file-scanner-gui
echo   Short:        ufs-gui
echo.
echo For more information, visit: https://github.com/yourusername/unsafe-file-scanner
pause
