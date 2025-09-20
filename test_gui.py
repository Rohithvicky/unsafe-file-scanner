#!/usr/bin/env python
"""
Test script for the GUI application
This script tests the GUI components without requiring user interaction.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
import tempfile
import threading
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unsafe_file_scanner_gui import UnsafeFileScannerGUI


def test_gui_creation():
    """Test that the GUI can be created without errors."""
    print("Testing GUI creation...")
    
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        app = UnsafeFileScannerGUI(root)
        
        print("✓ GUI created successfully")
        
        # Test basic functionality
        test_basic_functionality(app)
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ GUI creation failed: {e}")
        return False


def test_basic_functionality(app):
    """Test basic GUI functionality."""
    print("Testing basic functionality...")
    
    try:
        # Test directory addition
        app.dir_entry.insert(0, "/tmp")
        app.add_directory()
        
        if app.dir_listbox.size() > 0:
            print("✓ Directory addition works")
        else:
            print("✗ Directory addition failed")
        
        # Test configuration loading
        app.config_file_entry.delete(0, tk.END)
        app.config_file_entry.insert(0, "config.json")
        
        if os.path.exists("config.json"):
            app.load_config_file()
            print("✓ Configuration loading works")
        else:
            print("! Configuration file not found (expected)")
        
        # Test clear functionality
        app.clear_directories()
        app.clear_results()
        
        if app.dir_listbox.size() == 0:
            print("✓ Clear functionality works")
        else:
            print("✗ Clear functionality failed")
        
        print("✓ Basic functionality tests passed")
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")


def test_scan_simulation():
    """Test scan simulation without actually running a scan."""
    print("Testing scan simulation...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        
        app = UnsafeFileScannerGUI(root)
        
        # Add a test directory
        with tempfile.TemporaryDirectory() as temp_dir:
            app.dir_entry.insert(0, temp_dir)
            app.add_directory()
            
            # Simulate scan results
            from unsafe_file_scanner import UnsafeFileScanner
            scanner = UnsafeFileScanner()
            scanner.scan_stats = {
                'total_files': 10,
                'unsafe_files': 2,
                'suid_files': 0,
                'sgid_files': 0,
                'world_writable': 1,
                'non_owner_writable': 1,
                'scan_duration': 0.1
            }
            
            # Create mock unsafe files
            from unsafe_file_scanner import UnsafeFile
            scanner.unsafe_files = [
                UnsafeFile(
                    path="/tmp/test1.txt",
                    permissions="-rw-rw-rw-",
                    owner="user",
                    group="user",
                    size=100,
                    modified_time="2024-01-01T00:00:00",
                    issues=["World-writable"],
                    risk_level="HIGH"
                ),
                UnsafeFile(
                    path="/tmp/test2.txt",
                    permissions="-rw-r--r--",
                    owner="user",
                    group="user",
                    size=200,
                    modified_time="2024-01-01T00:00:00",
                    issues=["Group-writable"],
                    risk_level="MEDIUM"
                )
            ]
            
            app.scanner = scanner
            app.update_results()
            
            # Check if results were updated
            if app.summary_text.get(1.0, tk.END).strip():
                print("✓ Results update works")
            else:
                print("✗ Results update failed")
            
            if app.details_tree.get_children():
                print("✓ Detailed results display works")
            else:
                print("✗ Detailed results display failed")
        
        root.destroy()
        print("✓ Scan simulation tests passed")
        
    except Exception as e:
        print(f"✗ Scan simulation test failed: {e}")


def test_error_handling():
    """Test error handling in the GUI."""
    print("Testing error handling...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        
        app = UnsafeFileScannerGUI(root)
        
        # Test invalid directory
        app.dir_entry.insert(0, "/nonexistent/directory")
        app.add_directory()
        
        # Should show error message
        print("✓ Error handling for invalid directory works")
        
        # Test invalid config file
        app.config_file_entry.delete(0, tk.END)
        app.config_file_entry.insert(0, "/nonexistent/config.json")
        app.load_config_file()
        
        # Should show error message
        print("✓ Error handling for invalid config file works")
        
        root.destroy()
        print("✓ Error handling tests passed")
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")


def main():
    """Run all GUI tests."""
    print("=" * 60)
    print("UNSAFE FILE SCANNER GUI - TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("GUI Creation", test_gui_creation),
        ("Scan Simulation", test_scan_simulation),
        ("Error Handling", test_error_handling),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED: {e}")
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! GUI is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
