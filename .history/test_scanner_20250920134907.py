#!/usr/bin/env python3
"""
Test script for Unsafe File Scanner
This script creates test files with various permission issues for testing purposes.
"""

import os
import stat
import tempfile
import shutil
from pathlib import Path
from unsafe_file_scanner import UnsafeFileScanner


def create_test_files(test_dir: str):
    """Create test files with various permission issues."""
    print(f"Creating test files in: {test_dir}")
    
    # Create a normal file
    normal_file = os.path.join(test_dir, "normal_file.txt")
    with open(normal_file, "w") as f:
        f.write("This is a normal file")
    os.chmod(normal_file, 0o644)
    
    # Create a world-writable file
    world_writable = os.path.join(test_dir, "world_writable.txt")
    with open(world_writable, "w") as f:
        f.write("This file is world-writable")
    os.chmod(world_writable, 0o666)
    
    # Create a SUID file (simulated)
    suid_file = os.path.join(test_dir, "suid_file")
    with open(suid_file, "w") as f:
        f.write("#!/bin/bash\necho 'This is a SUID file'")
    os.chmod(suid_file, 0o4755)  # SUID bit set
    
    # Create a SGID file (simulated)
    sgid_file = os.path.join(test_dir, "sgid_file")
    with open(sgid_file, "w") as f:
        f.write("#!/bin/bash\necho 'This is a SGID file'")
    os.chmod(sgid_file, 0o2755)  # SGID bit set
    
    # Create a file writable by group but not owner
    group_writable = os.path.join(test_dir, "group_writable.txt")
    with open(group_writable, "w") as f:
        f.write("This file is group-writable but not owner-writable")
    os.chmod(group_writable, 0o464)  # Group write, not owner write
    
    # Create a directory with unusual permissions
    unusual_dir = os.path.join(test_dir, "unusual_dir")
    os.makedirs(unusual_dir, exist_ok=True)
    os.chmod(unusual_dir, 0o777)  # World-writable directory
    
    # Create a file in the unusual directory
    unusual_file = os.path.join(unusual_dir, "file_in_unusual_dir.txt")
    with open(unusual_file, "w") as f:
        f.write("File in unusual directory")
    os.chmod(unusual_file, 0o644)
    
    print("Test files created successfully!")


def run_test_scan(test_dir: str):
    """Run the scanner on the test directory."""
    print(f"\nRunning scanner on: {test_dir}")
    
    # Create scanner instance
    scanner = UnsafeFileScanner()
    
    # Run the scan
    scanner.run_scan([test_dir])
    
    return scanner


def main():
    """Main test function."""
    print("Unsafe File Scanner - Test Script")
    print("=" * 50)
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        
        # Create test files
        create_test_files(temp_dir)
        
        # Run the scanner
        scanner = run_test_scan(temp_dir)
        
        # Print detailed results
        if scanner.unsafe_files:
            print(f"\nDetailed Results:")
            print("-" * 60)
            for file in scanner.unsafe_files:
                print(f"File: {file.path}")
                print(f"  Permissions: {file.permissions}")
                print(f"  Owner: {file.owner}, Group: {file.group}")
                print(f"  Risk Level: {file.risk_level}")
                print(f"  Issues: {', '.join(file.issues)}")
                print()
        
        # Generate and save report
        report = scanner.generate_report()
        report_file = "test_scan_report.json"
        scanner.save_report(report, report_file)
        print(f"Test report saved to: {report_file}")


if __name__ == "__main__":
    main()
