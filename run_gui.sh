#!/bin/bash
# Unsafe File Scanner GUI Launcher
# This script launches the GUI application

echo "Starting Unsafe File Scanner GUI..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Error: Python is not installed or not in PATH"
        echo "Please install Python and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if tkinter is available
$PYTHON_CMD -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: tkinter is not available"
    echo "Please install Python with tkinter support"
    echo "On Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "On CentOS/RHEL: sudo yum install tkinter"
    echo "On macOS: tkinter should be included with Python"
    exit 1
fi

# Check if the main scanner module exists
if [ ! -f "unsafe_file_scanner.py" ]; then
    echo "Error: unsafe_file_scanner.py not found"
    echo "Please run from the correct directory"
    exit 1
fi

# Run the GUI
$PYTHON_CMD run_gui.py

# Check exit status
if [ $? -ne 0 ]; then
    echo
    echo "An error occurred. Check the output above for details."
    exit 1
fi


