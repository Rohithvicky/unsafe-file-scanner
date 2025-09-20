#!/usr/bin/env python3
"""
Test script to verify installation
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from unsafe_file_scanner.unsafe_file_scanner import main as cli_main
    from unsafe_file_scanner.unsafe_file_scanner_gui import main as gui_main
    
    print("✅ Package imports successful!")
    print("✅ CLI module imported successfully!")
    print("✅ GUI module imported successfully!")
    
    # Test CLI help
    print("\n🔧 Testing CLI help...")
    sys.argv = ['test_install.py', '--help']
    cli_main()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
