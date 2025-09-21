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

Author: Rohith Vicky
Version: 1.0.0
License: MIT
"""

from .unsafe_file_scanner import UnsafeFileScanner, UnsafeFile

# Try to import GUI components (may fail in headless environments)
try:
    from .unsafe_file_scanner_gui import main as gui_main
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    gui_main = None

# Try to import real-time monitoring (requires watchdog)
try:
    from .realtime_monitor import RealTimeMonitorGUI
    REALTIME_AVAILABLE = True
except ImportError:
    REALTIME_AVAILABLE = False
    RealTimeMonitorGUI = None

# Try to import rule engine
try:
    from .rule_engine import RuleEngine
    RULE_ENGINE_AVAILABLE = True
except ImportError:
    RULE_ENGINE_AVAILABLE = False
    RuleEngine = None

__version__ = "1.0.0"
__author__ = "Rohith Vicky"
__email__ = "rohithvicky@example.com"
__license__ = "MIT"

__all__ = [
    "UnsafeFileScanner",
    "UnsafeFile", 
    "gui_main",
    "RealTimeMonitorGUI",
    "RuleEngine",
    "GUI_AVAILABLE",
    "REALTIME_AVAILABLE", 
    "RULE_ENGINE_AVAILABLE"
]

# Package metadata
__title__ = "unsafe-file-scanner"
__description__ = "Professional Security Tool for File Permission Analysis"
__url__ = "https://github.com/Rohithvicky/unsafe-file-scanner"
__download_url__ = f"{__url__}/archive/v{__version__}.tar.gz"
__keywords__ = [
    "security", "file-permissions", "linux", "suid", "sgid", 
    "world-writable", "privilege-escalation", "file-integrity", "monitoring",
    "file-system", "permission-analysis", "security-audit", "system-administration",
    "gui", "cli", "real-time-monitoring"
]
__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: System Administrators",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Developers",
    "Topic :: Security",
    "Topic :: System :: Systems Administration",
    "Topic :: System :: Monitoring",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Environment :: Console",
    "Environment :: X11 Applications :: Qt",
    "Natural Language :: English",
]
