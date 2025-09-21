# 🔒 Unsafe File Scanner - Technical Documentation

## 1. Importing Required Libraries

### Core Libraries
```python
import os
import sys
import stat
import argparse
import logging
import json
import time
import csv
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
```

**Fig 1: Core Libraries**
- `os` → for file system operations and path manipulation
- `stat` → for file permission and metadata analysis
- `pathlib` → for modern path handling and file operations
- `typing` → for type hints and better code documentation
- `dataclasses` → for creating structured data classes
- `json` → for configuration and report serialization
- `csv` → for CSV report generation
- `logging` → for comprehensive audit trails and debugging

### GUI Libraries
```python
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import webbrowser
```

**Fig 2: GUI Libraries**
- `tkinter` → for building the main GUI window and widgets
- `tkinter.ttk` → provides themed widgets with modern styling
- `tkinter.filedialog` → for file and directory selection dialogs
- `tkinter.messagebox` → for user notifications and confirmations
- `tkinter.scrolledtext` → for scrollable text areas
- `threading` → for non-blocking GUI operations
- `webbrowser` → for opening generated HTML reports

### Advanced Features Libraries
```python
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
```

**Fig 3: Advanced Libraries**
- `watchdog` → for real-time file system monitoring
- `pwd` & `grp` → for Unix user/group information (Linux/macOS)
- `fnmatch` → for pattern matching in file paths
- `re` → for regular expression pattern matching

## 2. Core Security Analysis Modules

### 2.1. File Permission Scanner

**Fig 4: File Permission Scanner**
```python
class UnsafeFileScanner:
    def scan_file(self, file_path: str) -> Optional[UnsafeFile]:
        """Scan a single file for unsafe permissions."""
        # Get file permissions and metadata
        permissions, owner, group, size = self.get_file_permissions(file_path)
        
        # Check for various security issues
        all_issues = []
        all_issues.extend(self.check_suid_sgid(file_path, stat_info))
        all_issues.extend(self.check_world_writable(file_path, stat_info))
        all_issues.extend(self.check_non_owner_writable(file_path, stat_info))
        all_issues.extend(self.check_other_permissions(file_path, stat_info))
        
        # Apply rule engine if available
        if self.rule_engine:
            rule_matches = self.rule_engine.evaluate_file(file_path, file_info)
        
        # Assess risk level and create unsafe file record
        risk_level = self.assess_risk_level(all_issues)
        return UnsafeFile(...)
```

**Process Handling & Analysis:**
- Recursively scans directories using `os.walk()`
- Analyzes each file's permissions using `os.stat()`
- Checks for SUID/SGID bits, world-writable permissions, and other anomalies
- Applies advanced rule engine for custom security checks
- Categorizes findings by risk level (CRITICAL, HIGH, MEDIUM, LOW)

### 2.2. SUID/SGID Detection

**Fig 5: SUID/SGID Detection**
```python
def check_suid_sgid(self, file_path: str, stat_info: os.stat_result) -> List[str]:
    """Check for SUID and SGID bits."""
    issues = []
    mode = stat_info.st_mode
    
    if mode & stat.S_ISUID:
        issues.append("SUID bit set")
    
    if mode & stat.S_ISGID:
        issues.append("SGID bit set")
    
    return issues
```

**Security Analysis:**
- **SUID Detection**: Identifies files with Set User ID bit that execute with owner's privileges
- **SGID Detection**: Finds files with Set Group ID bit that execute with group's privileges
- **Risk Assessment**: Both SUID and SGID files are classified as HIGH risk
- **Cross-platform**: Adapts detection logic for Windows vs Unix systems

### 2.3. World-Writable File Detection

**Fig 6: World-Writable Detection**
```python
def check_world_writable(self, file_path: str, stat_info: os.stat_result) -> List[str]:
    """Check if file is world-writable."""
    issues = []
    
    if not UNIX_PLATFORM:
        # Windows-specific checks
        try:
            with open(file_path, 'a'):
                pass
            if any(public in file_path.lower() for public in ['public', 'shared', 'temp']):
                issues.append("Potentially world-writable (Windows)")
        except (OSError, PermissionError):
            pass
    else:
        # Unix-specific checks
        mode = stat_info.st_mode
        if mode & stat.S_IWOTH:  # World write permission
            issues.append("World-writable")
    
    return issues
```

**Security Analysis:**
- **Unix Systems**: Checks for world write permission (S_IWOTH bit)
- **Windows Systems**: Attempts to write to file and checks location patterns
- **Risk Level**: World-writable files are classified as HIGH risk
- **Context Awareness**: Considers file location and type for risk assessment

### 2.4. Non-Owner Writable Detection

**Fig 7: Non-Owner Writable Detection**
```python
def check_non_owner_writable(self, file_path: str, stat_info: os.stat_result) -> List[str]:
    """Check if file is writable by non-owners."""
    issues = []
    mode = stat_info.st_mode
    
    # Check if group has write permission but owner doesn't
    if mode & stat.S_IWGRP and not (mode & stat.S_IWUSR):
        issues.append("Group-writable but not owner-writable")
    
    # Check if others have write permission but owner doesn't
    if mode & stat.S_IWOTH and not (mode & stat.S_IWUSR):
        issues.append("Others-writable but not owner-writable")
    
    return issues
```

**Security Analysis:**
- **Permission Anomalies**: Detects unusual permission combinations
- **Group Write**: Files writable by group but not owner
- **Others Write**: Files writable by others but not owner
- **Risk Assessment**: Classified as MEDIUM risk level

### 2.5. Advanced Permission Analysis

**Fig 8: Advanced Permission Analysis**
```python
def check_other_permissions(self, file_path: str, stat_info: os.stat_result) -> List[str]:
    """Check for other permission-related issues."""
    issues = []
    mode = stat_info.st_mode
    
    # Check for files with execute permission but no read permission
    if mode & stat.S_IXUSR and not (mode & stat.S_IRUSR):
        issues.append("Executable but not readable by owner")
    
    # Check for directories with unusual permissions
    if stat.S_ISDIR(mode):
        if not (mode & stat.S_IRUSR):
            issues.append("Directory not readable by owner")
        if not (mode & stat.S_IXUSR):
            issues.append("Directory not executable by owner")
    
    return issues
```

**Security Analysis:**
- **Executable Anomalies**: Files that can be executed but not read
- **Directory Issues**: Directories without proper read/execute permissions
- **Permission Logic**: Validates logical permission combinations
- **Risk Assessment**: Classified as MEDIUM risk level

## 3. Advanced Rule Engine

### 3.1. Rule Engine Architecture

**Fig 9: Rule Engine Architecture**
```python
class RuleEngine:
    def __init__(self, rules_file: Optional[str] = None):
        self.rules: List[SecurityRule] = []
        self.custom_functions: Dict[str, Callable] = {}
        self._load_default_rules()
        
        if rules_file and os.path.exists(rules_file):
            self.load_rules_from_file(rules_file)
```

**Rule Management:**
- **Default Rules**: 15+ built-in security rules covering common vulnerabilities
- **Custom Rules**: Support for user-defined security patterns
- **Rule Types**: Permission, path pattern, file extension, file size, owner/group
- **Risk Levels**: CRITICAL, HIGH, MEDIUM, LOW, INFO classification

### 3.2. Built-in Security Rules

**Fig 10: Built-in Security Rules**
```python
default_rules = [
    # SUID/SGID rules
    SecurityRule(
        id="suid_executable",
        name="SUID Executable",
        description="Files with SUID bit set",
        rule_type=RuleType.PERMISSION,
        pattern="suid",
        risk_level=RiskLevel.HIGH
    ),
    
    # World-writable rules
    SecurityRule(
        id="world_writable_sensitive",
        name="World Writable Sensitive File",
        description="Sensitive files that are world-writable",
        rule_type=RuleType.PATH_PATTERN,
        pattern="**/passwd*,**/shadow*,**/hosts*,**/ssh/**",
        risk_level=RiskLevel.CRITICAL
    ),
    
    # File extension rules
    SecurityRule(
        id="script_world_writable",
        name="Script World Writable",
        description="Executable scripts that are world-writable",
        rule_type=RuleType.FILE_EXTENSION,
        pattern="*.sh,*.py,*.pl,*.rb,*.js,*.php",
        risk_level=RiskLevel.HIGH
    )
]
```

**Rule Categories:**
- **Permission Rules**: SUID/SGID, world-writable, permission anomalies
- **Path Pattern Rules**: Sensitive file locations, temporary directories
- **File Extension Rules**: Scripts, config files, executables
- **File Size Rules**: Large files with dangerous permissions
- **Owner/Group Rules**: Root-owned files with world access

### 3.3. Rule Evaluation Engine

**Fig 11: Rule Evaluation Engine**
```python
def evaluate_file(self, file_path: str, file_info: Dict[str, Any]) -> List[RuleMatch]:
    """Evaluate a file against all enabled rules."""
    matches = []
    
    for rule in self.rules:
        if not rule.enabled:
            continue
            
        try:
            match = self._evaluate_rule(rule, file_path, file_info)
            if match:
                matches.append(match)
        except Exception as e:
            self.logger.error(f"Error evaluating rule {rule.id}: {e}")
    
    return matches
```

**Evaluation Process:**
- **Rule Filtering**: Only processes enabled rules
- **Type-specific Evaluation**: Different logic for each rule type
- **Error Handling**: Graceful handling of rule evaluation errors
- **Result Aggregation**: Collects all matching rules for a file

## 4. Real-time Monitoring System

### 4.1. File System Event Handler

**Fig 12: File System Event Handler**
```python
class UnsafeFileEventHandler(FileSystemEventHandler):
    def __init__(self, scanner, callback: Optional[Callable] = None):
        self.scanner = scanner
        self.callback = callback
    
    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory:
            self._check_file(event.src_path)
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory:
            self._check_file(event.src_path)
```

**Event Processing:**
- **File Creation**: Monitors new files for immediate security analysis
- **File Modification**: Re-checks files when permissions change
- **File Movement**: Tracks files moved or renamed
- **Real-time Analysis**: Instant security assessment of file changes

### 4.2. Real-time Monitor

**Fig 13: Real-time Monitor**
```python
class RealTimeMonitor:
    def start_monitoring(self, directories: List[str]) -> None:
        """Start monitoring specified directories."""
        self.observer = Observer()
        event_handler = UnsafeFileEventHandler(self.scanner, self.callback)
        
        for directory in directories:
            if os.path.exists(directory) and os.path.isdir(directory):
                self.observer.schedule(event_handler, directory, recursive=True)
                self.monitored_dirs.append(directory)
        
        if self.monitored_dirs:
            self.observer.start()
            self.is_monitoring = True
```

**Monitoring Features:**
- **Recursive Monitoring**: Watches entire directory trees
- **Multi-directory Support**: Can monitor multiple directories simultaneously
- **Thread Safety**: Runs in separate thread to avoid blocking GUI
- **Status Tracking**: Maintains monitoring state and directory list

## 5. GUI Interface Components

### 5.1. Modern GUI Design

**Fig 14: Modern GUI Design**
```python
class UnsafeFileScannerGUI:
    def create_modern_widgets(self):
        # Modern dark theme configuration
        self.root.configure(bg='#0d1117')
        
        # Modern header section with glassmorphism effect
        self.header_frame = tk.Frame(self.main_frame, bg='#161b22', relief='flat', bd=0)
        
        # Modern title with premium typography
        self.title_label = tk.Label(
            self.header_frame, 
            text="🔒 Unsafe File Scanner", 
            font=("SF Pro Display", 28, "bold"),
            fg='#ffffff',
            bg='#161b22'
        )
```

**Design Elements:**
- **Dark Theme**: Professional dark color scheme (#0d1117, #161b22)
- **Modern Typography**: SF Pro Display font family for premium look
- **Glassmorphism Effects**: Subtle transparency and modern card designs
- **Responsive Layout**: Two-panel layout with configuration and results

### 5.2. Scan Configuration Panel

**Fig 15: Scan Configuration Panel**
```python
# Modern directory selection with sleek design
self.dir_frame = tk.Frame(self.left_panel, bg='#161b22')
self.dir_entry = tk.Entry(
    self.dir_frame, 
    width=45, 
    font=("SF Pro Text", 12),
    bg='#21262d',
    fg='#ffffff',
    insertbackground='#ffffff',
    relief='flat',
    bd=8
)

# Modern browse button
self.dir_browse_btn = tk.Button(
    self.dir_frame, 
    text="📁 Select", 
    command=self.browse_directories,
    font=("SF Pro Text", 11, "bold"),
    bg='#238636',
    fg='#ffffff',
    relief='flat',
    bd=0,
    padx=12,
    pady=5,
    cursor='hand2'
)
```

**Configuration Features:**
- **Directory Selection**: Browse and select target directories
- **Output File**: Specify where to save scan results
- **Export Format**: Choose between JSON, CSV, or HTML
- **Advanced Options**: Real-time monitoring and rule management

### 5.3. Results Display System

**Fig 16: Results Display System**
```python
# Results tabs
self.results_notebook = ttk.Notebook(self.right_panel)

# Summary tab
self.summary_tab = ttk.Frame(self.results_notebook)
self.summary_text = scrolledtext.ScrolledText(
    self.summary_tab, 
    height=12, 
    wrap=tk.WORD
)

# Detailed results tab
self.details_tab = ttk.Frame(self.results_notebook)
self.details_tree = ttk.Treeview(
    self.details_tab,
    columns=("path", "permissions", "owner", "group", "risk", "issues"),
    show="headings",
    height=12
)
```

**Display Features:**
- **Tabbed Interface**: Summary, detailed results, and raw JSON views
- **Summary View**: Overview of scan statistics and risk breakdown
- **Detailed Table**: Sortable table with all unsafe files
- **Raw JSON**: Complete scan data for technical analysis

## 6. Export and Reporting System

### 6.1. Multi-format Export

**Fig 17: Multi-format Export**
```python
def save_report(self, report: Dict, output_file: str) -> None:
    """Save the scan report to a file."""
    file_ext = Path(output_file).suffix.lower()
    
    if file_ext == '.csv':
        self._save_csv_report(report, output_file)
    elif file_ext == '.html':
        self._save_html_report(report, output_file)
    else:
        # Default to JSON
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
```

**Export Formats:**
- **JSON**: Machine-readable format for integration
- **CSV**: Spreadsheet-compatible format for analysis
- **HTML**: Professional web report with styling

### 6.2. HTML Report Generation

**Fig 18: HTML Report Generation**
```python
def _save_html_report(self, report: Dict, output_file: str) -> None:
    """Save report in HTML format."""
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Unsafe File Scanner Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        .header {{ text-align: center; color: #2c3e50; border-bottom: 3px solid #3498db; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .stat-card {{ background: white; padding: 15px; border-radius: 5px; text-align: center; }}
        .risk-high {{ color: #e74c3c; font-weight: bold; }}
        .risk-medium {{ color: #f39c12; font-weight: bold; }}
        .risk-low {{ color: #27ae60; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Unsafe File Scanner Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        <!-- Report content -->
    </div>
</body>
</html>
"""
```

**HTML Features:**
- **Professional Styling**: Modern CSS with responsive design
- **Interactive Elements**: Sortable tables and expandable sections
- **Risk Color Coding**: Visual indicators for different risk levels
- **Statistics Dashboard**: Summary cards with key metrics

## 7. Functions and Buttons

### 7.1. Core Scan Functions

**Fig 19: Core Scan Functions**
```python
def start_scan(self):
    """Start the scan process."""
    # Get directory to scan
    directory = self.dir_entry.get().strip()
    if not directory:
        messagebox.showerror("Error", "Please select a directory to scan")
        return
    
    # Update UI
    self.is_scanning = True
    self.scan_btn.config(state="disabled")
    self.stop_btn.config(state="normal")
    self.progress_bar.start()
    self.status_indicator.config(text="● Scanning...", foreground="#3498db")
    
    # Start scan in separate thread
    self.scan_thread = threading.Thread(target=self.run_scan, args=(directories,))
    self.scan_thread.daemon = True
    self.scan_thread.start()
```

**Scan Management:**
- **Validation**: Checks directory existence and permissions
- **UI Updates**: Disables controls and shows progress
- **Threading**: Runs scan in background to keep GUI responsive
- **Error Handling**: Displays user-friendly error messages

### 7.2. Real-time Monitoring Functions

**Fig 20: Real-time Monitoring Functions**
```python
def toggle_realtime_monitoring(self):
    """Toggle real-time monitoring."""
    if not self.is_monitoring:
        # Start monitoring
        directories = [self.dir_entry.get().strip()]
        
        if not self.realtime_monitor:
            self.realtime_monitor = RealTimeMonitorGUI(
                self.scanner, 
                self.on_realtime_alert
            )
        
        self.realtime_monitor.start_monitoring(directories)
        self.is_monitoring = True
        self.realtime_btn.config(text="⏹️ Stop Monitor")
        self.status_indicator.config(text="● Monitoring...", foreground="#e74c3c")
    else:
        # Stop monitoring
        self.realtime_monitor.stop_monitoring()
        self.is_monitoring = False
        self.realtime_btn.config(text="👁️ Start Real-time Monitor")
        self.status_indicator.config(text="● Ready", foreground="#27ae60")
```

**Monitoring Features:**
- **Toggle Control**: Start/stop monitoring with single button
- **Status Updates**: Visual indicators for monitoring state
- **Alert Handling**: Processes real-time security alerts
- **Result Management**: Accumulates and displays monitoring results

### 7.3. Export and Management Functions

**Fig 21: Export and Management Functions**
```python
def export_results(self):
    """Export results to file."""
    if not self.scanner:
        messagebox.showerror("Error", "No results to export")
        return
    
    # Get selected export format
    export_format = self.export_format_combo.get().lower()
    
    # Set default extension based on format
    if export_format == "json":
        default_ext = ".json"
        filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
    elif export_format == "csv":
        default_ext = ".csv"
        filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
    elif export_format == "html":
        default_ext = ".html"
        filetypes = [("HTML files", "*.html"), ("All files", "*.*")]
    
    filename = filedialog.asksaveasfilename(
        title="Export Results",
        defaultextension=default_ext,
        filetypes=filetypes
    )
    
    if filename:
        # Generate and save report
        report = self.scanner.generate_report()
        self.scanner.save_report(report, filename)
        messagebox.showinfo("Success", f"Results exported to {filename}")
```

**Export Features:**
- **Format Selection**: Choose between JSON, CSV, or HTML
- **File Dialog**: User-friendly file selection interface
- **Error Handling**: Validates data availability and file access
- **Success Feedback**: Confirmation messages for completed operations

## 8. Tkinter GUI Setup

### 8.1. Modern Theme Configuration

**Fig 22: Modern Theme Configuration**
```python
def apply_modern_theme(self):
    """Apply modern 2025 theme with hover effects and animations."""
    # Configure button hover effects
    def add_hover_effect(button, hover_color, normal_color):
        def on_enter(e):
            button.config(bg=hover_color)
        def on_leave(e):
            button.config(bg=normal_color)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    # Apply hover effects to buttons with professional colors
    add_hover_effect(self.dir_browse_btn, '#2ea043', '#238636')
    add_hover_effect(self.scan_btn, '#2ea043', '#238636')
    add_hover_effect(self.stop_btn, '#f85149', '#da3633')
    add_hover_effect(self.clear_btn, '#8b5cf6', '#6f42c1')
```

**Theme Features:**
- **Hover Effects**: Interactive button animations
- **Color Scheme**: Professional dark theme with accent colors
- **Focus States**: Visual feedback for input fields
- **Consistent Styling**: Unified design language throughout

### 8.2. Layout Management

**Fig 23: Layout Management**
```python
def setup_modern_layout(self):
    """Setup modern 2025-style layout."""
    # Main frame with modern spacing
    self.main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Modern header section with compact padding
    self.header_frame.pack(fill=tk.X, pady=(0, 15), padx=15)
    
    # Modern content area with side-by-side layout
    self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    # Modern left panel with card-like appearance
    self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
    
    # Modern right panel - Results
    self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
```

**Layout Structure:**
- **Header Section**: Title, subtitle, and status indicator
- **Left Panel**: Configuration controls and advanced features
- **Right Panel**: Results display with tabbed interface
- **Status Bar**: Bottom status information

### 8.3. Professional Styling

**Fig 24: Professional Styling**
```python
# Modern status indicator with animated appearance
self.status_indicator = tk.Label(
    self.header_frame,
    text="● Ready to Scan",
    font=("SF Pro Text", 12, "bold"),
    fg='#3fb950',
    bg='#161b22'
)

# Modern control buttons section
self.scan_btn = tk.Button(
    self.control_frame, 
    text="🚀 Start Security Scan", 
    command=self.start_scan,
    font=("SF Pro Text", 11, "bold"),
    bg='#238636',
    fg='#ffffff',
    relief='flat',
    bd=0,
    padx=20,
    pady=8,
    cursor='hand2'
)
```

**Styling Elements:**
- **Typography**: SF Pro font family for modern appearance
- **Color Coding**: Green for ready/success, red for errors, blue for info
- **Icons**: Emoji icons for visual clarity
- **Spacing**: Consistent padding and margins
- **Cursors**: Hand cursor for clickable elements

## 9. Performance and Security Features

### 9.1. Cross-platform Compatibility

**Fig 25: Cross-platform Compatibility**
```python
# Platform-specific imports
try:
    import pwd
    import grp
    UNIX_PLATFORM = True
except ImportError:
    # Windows or other non-Unix platform
    pwd = None
    grp = None
    UNIX_PLATFORM = False
```

**Platform Support:**
- **Windows**: Adapted permission checks for Windows file system
- **Linux**: Full Unix permission analysis with SUID/SGID detection
- **macOS**: Native Unix compatibility with macOS-specific considerations
- **Graceful Degradation**: Features adapt based on platform capabilities

### 9.2. Memory and Performance Optimization

**Fig 26: Performance Optimization**
```python
def scan_file(self, file_path: str) -> Optional[UnsafeFile]:
    """Scan a single file for unsafe permissions."""
    try:
        # Check file size limit
        if os.path.getsize(file_path) > self.config['max_file_size']:
            self.logger.debug(f"Skipping large file: {file_path}")
            return None
        
        # Process file without loading into memory
        stat_info = os.stat(file_path, follow_symlinks=self.config['follow_symlinks'])
        # ... analysis continues
```

**Optimization Features:**
- **File Size Limits**: Configurable maximum file size to prevent memory issues
- **Streaming Processing**: Processes files without loading entire content
- **Exclusion Patterns**: Skips unnecessary files and directories
- **Progress Tracking**: Real-time progress updates for long scans

### 9.3. Security and Logging

**Fig 27: Security and Logging**
```python
def setup_logging(self):
    """Setup logging configuration."""
    log_level = getattr(logging, self.config['log_level'].upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('unsafe_file_scanner.log')
        ]
    )
    self.logger = logging.getLogger(__name__)
```

**Security Features:**
- **Comprehensive Logging**: All operations logged for audit trails
- **Error Handling**: Graceful handling of permission errors and file access issues
- **Input Validation**: Validates all user inputs and file paths
- **Safe File Operations**: Uses safe file handling practices

## 10. Advanced Features Summary

### 10.1. Core Security Analysis
- **SUID/SGID Detection**: Identifies privilege escalation risks
- **World-writable Files**: Detects files accessible by all users
- **Permission Anomalies**: Finds unusual permission combinations
- **Risk Assessment**: Categorizes findings by security impact

### 10.2. Real-time Monitoring
- **Live Detection**: Instant notification of security threats
- **File System Events**: Monitors file creation, modification, and movement
- **Alert Management**: Accumulates and manages real-time findings
- **Background Processing**: Non-blocking monitoring operations

### 10.3. Professional GUI
- **Modern Design**: Dark theme with professional styling
- **Intuitive Interface**: Two-panel layout with clear navigation
- **Real-time Updates**: Live status indicators and progress tracking
- **Export Options**: Multiple format support for different use cases

### 10.4. Advanced Rule Engine
- **15+ Built-in Rules**: Comprehensive security rule set
- **Custom Rules**: Support for user-defined security patterns
- **Rule Management**: Enable/disable rules and save configurations
- **Risk Classification**: Multi-level risk assessment system

---

**🔒 Unsafe File Scanner - Professional Security Tool for File Permission Analysis**

*Built with Python, featuring modern GUI design, real-time monitoring, and comprehensive security analysis capabilities.*
