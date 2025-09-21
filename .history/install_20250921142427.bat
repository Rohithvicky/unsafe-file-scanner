@echo off
REM Professional Installation Script for Unsafe File Scanner (Windows)
REM Supports Windows 10/11 with Python 3.8+

setlocal enabledelayedexpansion

echo.
echo 🔒 Unsafe File Scanner - Professional Installation Script
echo =========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed.
    echo.
    echo Please install Python 3.8 or higher:
    echo   Download from: https://www.python.org/downloads/
    echo   Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed.
    echo.
    echo Please install pip:
    echo   python -m ensurepip --upgrade
    echo   Or reinstall Python with pip included
    echo.
    pause
    exit /b 1
)

echo ✅ pip found

REM Check if we're in the right directory
if not exist "setup.py" (
    echo ❌ setup.py not found.
    echo Please run this script from the Unsafe File Scanner root directory.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt not found.
    echo Please run this script from the Unsafe File Scanner root directory.
    pause
    exit /b 1
)

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Install the package
echo 📦 Installing Unsafe File Scanner...
pip install -e .

if %errorlevel% equ 0 (
    echo.
    echo ✅ Installation completed successfully!
    echo.
    echo 🚀 Usage Examples:
    echo   Command Line: unsafe-file-scanner C:\path\to\scan
    echo   GUI:          unsafe-file-scanner-gui
    echo   Short CLI:    ufs C:\path\to\scan
    echo   Short GUI:    ufs-gui
    echo.
    echo 📖 Documentation:
    echo   README:       type README.md
    echo   Help:         unsafe-file-scanner --help
    echo.
    echo 🔧 Development:
    echo   Install dev:  pip install -r requirements-dev.txt
    echo   Run tests:    pytest
    echo.
    
    REM Check if GUI is available
    python -c "import tkinter" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ GUI support available
    ) else (
        echo ⚠️  GUI support not available (tkinter not found)
        echo   Install GUI: pip install tk
    )
    
    REM Check if watchdog is available
    python -c "import watchdog" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Real-time monitoring available
    ) else (
        echo ⚠️  Real-time monitoring not available (watchdog not installed)
    )
    
    REM Create desktop shortcut
    echo 🖥️ Creating desktop shortcut...
    set "desktop=%USERPROFILE%\Desktop"
    set "shortcut=%desktop%\Unsafe File Scanner.lnk"
    
    REM Create a batch file to run the GUI
    echo @echo off > "unsafe-file-scanner-gui.bat"
    echo unsafe-file-scanner-gui >> "unsafe-file-scanner-gui.bat"
    
    REM Try to create a proper shortcut using PowerShell
    powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = 'unsafe-file-scanner-gui'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'Professional Security Analysis & File Permission Monitoring'; $Shortcut.Save()}" >nul 2>&1
    
    if exist "%shortcut%" (
        echo ✅ Desktop shortcut created
    ) else (
        echo ⚠️  Could not create desktop shortcut (PowerShell may be restricted)
    )
    
    echo.
    echo 🎉 Setup complete! You can now use Unsafe File Scanner.
    echo.
    echo For more information, visit: https://github.com/Rohithvicky/unsafe-file-scanner
    
) else (
    echo ❌ Installation failed!
    echo Please check the error messages above and try again.
)

echo.
pause