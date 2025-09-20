"""
Unsafe File Scanner - Professional Security Tool

A comprehensive file integrity monitoring and security analysis tool
for detecting unsafe file permissions and security vulnerabilities.

Features:
- File permission analysis (SUID/SGID, world-writable, etc.)
- Real-time monitoring with watchdog
- Advanced rule engine for custom security checks
- Professional GUI interface
- Multi-format export (JSON, CSV, HTML)
- Cross-platform support (Windows, Linux, macOS)

Author: AI Assistant
Version: 1.0.0
License: MIT
"""

from .unsafe_file_scanner import UnsafeFileScanner, UnsafeFile
from .unsafe_file_scanner_gui import main as gui_main

__version__ = "1.0.0"
__author__ = "AI Assistant"
__email__ = "assistant@example.com"
__license__ = "MIT"

__all__ = [
    "UnsafeFileScanner",
    "UnsafeFile", 
    "gui_main"
]

# Package metadata
__title__ = "unsafe-file-scanner"
__description__ = "Professional Security Tool for File Permission Analysis"
__url__ = "https://github.com/Rohithvicky/unsafe-file-scanner"
__download_url__ = f"{__url__}/archive/v{__version__}.tar.gz"
__keywords__ = [
    "security", "file-permissions", "linux", "suid", "sgid", 
    "world-writable", "privilege-escalation", "file-integrity", "monitoring"
]
__classifiers__ = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: System Administrators",
    "Intended Audience :: Information Technology",
    "Topic :: Security",
    "Topic :: System :: Systems Administration",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
]
