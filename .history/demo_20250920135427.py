#!/usr/bin/env python3
"""
Demo script for Unsafe File Scanner
This script demonstrates various features and usage patterns.
"""

import os
import sys
import tempfile
import json
from pathlib import Path
from unsafe_file_scanner import UnsafeFileScanner


def demo_basic_usage():
    """Demonstrate basic usage of the scanner."""
    print("=" * 60)
    print("DEMO 1: Basic Usage")
    print("=" * 60)
    
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Creating test files in: {temp_dir}")
        
        # Create various test files
        test_files = [
            ("normal_file.txt", 0o644, "Normal file"),
            ("world_writable.txt", 0o666, "World-writable file"),
            ("suid_file", 0o4755, "SUID file"),
            ("sgid_file", 0o2755, "SGID file"),
            ("group_writable.txt", 0o464, "Group-writable file"),
        ]
        
        for filename, mode, description in test_files:
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, "w") as f:
                f.write(f"# {description}\nThis is a test file.")
            os.chmod(filepath, mode)
            print(f"  Created: {filename} ({oct(mode)}) - {description}")
        
        # Run scanner
        print(f"\nRunning scanner on: {temp_dir}")
        scanner = UnsafeFileScanner()
        scanner.run_scan([temp_dir])
        
        return scanner


def demo_configuration():
    """Demonstrate configuration usage."""
    print("\n" + "=" * 60)
    print("DEMO 2: Configuration Usage")
    print("=" * 60)
    
    # Create a custom configuration
    config = {
        "exclude_dirs": [".git", "node_modules"],
        "exclude_files": [".DS_Store", "*.tmp"],
        "max_file_size": 1024 * 1024,  # 1MB
        "log_level": "DEBUG",
        "risk_thresholds": {
            "high": ["suid", "sgid"],
            "medium": ["world_writable"],
            "low": ["other_issues"]
        }
    }
    
    # Save config to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f, indent=2)
        config_file = f.name
    
    print(f"Created custom config: {config_file}")
    print("Configuration:")
    print(json.dumps(config, indent=2))
    
    # Create test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a large file (should be skipped)
        large_file = os.path.join(temp_dir, "large_file.txt")
        with open(large_file, "w") as f:
            f.write("x" * (2 * 1024 * 1024))  # 2MB file
        os.chmod(large_file, 0o666)
        
        # Create a normal file
        normal_file = os.path.join(temp_dir, "normal.txt")
        with open(normal_file, "w") as f:
            f.write("Normal file")
        os.chmod(normal_file, 0o644)
        
        # Create a SUID file
        suid_file = os.path.join(temp_dir, "suid_file")
        with open(suid_file, "w") as f:
            f.write("#!/bin/bash\necho 'SUID file'")
        os.chmod(suid_file, 0o4755)
        
        print(f"\nCreated test files in: {temp_dir}")
        
        # Run scanner with custom config
        scanner = UnsafeFileScanner(config_file)
        scanner.run_scan([temp_dir])
        
        # Clean up
        os.unlink(config_file)
        
        return scanner


def demo_reporting():
    """Demonstrate reporting features."""
    print("\n" + "=" * 60)
    print("DEMO 3: Reporting Features")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files with different risk levels
        test_files = [
            ("high_risk.txt", 0o666, "HIGH"),
            ("medium_risk.txt", 0o464, "MEDIUM"),
            ("low_risk.txt", 0o644, "LOW"),
        ]
        
        for filename, mode, risk in test_files:
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, "w") as f:
                f.write(f"Test file with {risk} risk")
            os.chmod(filepath, mode)
        
        # Run scanner
        scanner = UnsafeFileScanner()
        scanner.run_scan([temp_dir])
        
        # Generate detailed report
        report = scanner.generate_report()
        
        # Save report
        report_file = "demo_report.json"
        scanner.save_report(report, report_file)
        
        print(f"Report saved to: {report_file}")
        print("\nReport Summary:")
        print(f"  Total files scanned: {report['statistics']['total_files']}")
        print(f"  Unsafe files found: {report['summary']['total_unsafe_files']}")
        print(f"  High risk: {report['summary']['high_risk_files']}")
        print(f"  Medium risk: {report['summary']['medium_risk_files']}")
        print(f"  Low risk: {report['summary']['low_risk_files']}")
        
        return scanner


def demo_error_handling():
    """Demonstrate error handling."""
    print("\n" + "=" * 60)
    print("DEMO 4: Error Handling")
    print("=" * 60)
    
    # Test with non-existent directory
    print("Testing with non-existent directory...")
    scanner = UnsafeFileScanner()
    scanner.run_scan(["/non/existent/directory"])
    
    # Test with file instead of directory
    print("\nTesting with file instead of directory...")
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        temp_file = f.name
        f.write("This is a file, not a directory")
    
    scanner.run_scan([temp_file])
    os.unlink(temp_file)
    
    # Test with permission denied (if possible)
    print("\nTesting with restricted directory...")
    scanner.run_scan(["/root"])  # This might fail on some systems
    
    return scanner


def main():
    """Run all demos."""
    print("Unsafe File Scanner - Demo Script")
    print("This script demonstrates various features of the scanner.")
    print()
    
    try:
        # Demo 1: Basic usage
        scanner1 = demo_basic_usage()
        
        # Demo 2: Configuration
        scanner2 = demo_configuration()
        
        # Demo 3: Reporting
        scanner3 = demo_reporting()
        
        # Demo 4: Error handling
        scanner4 = demo_error_handling()
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETED")
        print("=" * 60)
        print("All demos completed successfully!")
        print("\nKey features demonstrated:")
        print("  ✓ Basic file scanning")
        print("  ✓ Configuration management")
        print("  ✓ Report generation")
        print("  ✓ Error handling")
        print("  ✓ Risk level assessment")
        print("  ✓ SUID/SGID detection")
        print("  ✓ World-writable file detection")
        print("  ✓ Non-owner writable file detection")
        
    except Exception as e:
        print(f"\nDemo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
