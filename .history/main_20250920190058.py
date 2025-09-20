#!/usr/bin/env python3
"""
Main entry point for Unsafe File Scanner
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unsafe_file_scanner.unsafe_file_scanner import main as cli_main
from unsafe_file_scanner.unsafe_file_scanner_gui import main as gui_main

def main():
    """Main entry point - launches GUI by default"""
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        # Launch CLI version
        sys.argv.remove('--cli')
        cli_main()
    else:
        # Launch GUI version by default
        gui_main()

if __name__ == "__main__":
    main()
