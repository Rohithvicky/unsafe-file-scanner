#!/usr/bin/env python
"""
GUI Launcher for Unsafe File Scanner
This script launches the GUI application with proper error handling.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all required dependencies are available."""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def main():
    """Main function to launch the GUI."""
    print("Starting Unsafe File Scanner GUI...")
    
    # Check dependencies
    if not check_dependencies():
        print("Error: tkinter is not available. Please install Python with tkinter support.")
        sys.exit(1)
    
    # Check if the main scanner module exists
    if not os.path.exists("unsafe_file_scanner.py"):
        print("Error: unsafe_file_scanner.py not found. Please run from the correct directory.")
        sys.exit(1)
    
    try:
        # Import and run the GUI
        from unsafe_file_scanner_gui import main as gui_main
        gui_main()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        
        # Try to show error in a message box if possible
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("Error", f"Failed to start GUI: {e}")
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()

