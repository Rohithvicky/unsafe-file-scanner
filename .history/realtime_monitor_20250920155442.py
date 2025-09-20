#!/usr/bin/env python3
"""
Real-time File Monitoring Module for Unsafe File Scanner
Uses watchdog library for cross-platform file system monitoring
"""

import os
import time
import logging
import threading
from pathlib import Path
from typing import List, Dict, Callable, Optional
from datetime import datetime

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent, FileMovedEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    Observer = None
    FileSystemEventHandler = None
    FileCreatedEvent = None
    FileModifiedEvent = None
    FileMovedEvent = None


class UnsafeFileEventHandler(FileSystemEventHandler):
    """Event handler for file system changes that checks for unsafe permissions."""
    
    def __init__(self, scanner, callback: Optional[Callable] = None):
        self.scanner = scanner
        self.callback = callback
        self.logger = logging.getLogger(__name__)
        
    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory:
            self._check_file(event.src_path)
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory:
            self._check_file(event.src_path)
    
    def on_moved(self, event):
        """Handle file move/rename events."""
        if not event.is_directory:
            self._check_file(event.dest_path)
    
    def _check_file(self, file_path: str):
        """Check a single file for unsafe permissions."""
        try:
            # Check if file should be excluded
            if self._should_exclude_file(file_path):
                return
                
            # Get file info
            stat_info = os.stat(file_path, follow_symlinks=self.scanner.config['follow_symlinks'])
            permissions, owner, group, size = self.scanner.get_file_permissions(file_path, stat_info)
            
            # Check for security issues
            issues = []
            issues.extend(self.scanner.check_suid_sgid(file_path, stat_info))
            issues.extend(self.scanner.check_world_writable(file_path, stat_info))
            issues.extend(self.scanner.check_non_owner_writable(file_path, stat_info))
            issues.extend(self.scanner.check_other_permissions(file_path, stat_info))
            
            if issues:
                # Determine risk level
                risk_level = self.scanner.determine_risk_level(issues)
                
                # Create unsafe file object
                unsafe_file = self.scanner.UnsafeFile(
                    path=file_path,
                    permissions=permissions,
                    owner=owner,
                    group=group,
                    size=size,
                    modified_time=datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    issues=issues,
                    risk_level=risk_level
                )
                
                # Add to scanner results
                self.scanner.unsafe_files.append(unsafe_file)
                self.scanner.scan_stats['unsafe_files'] += 1
                
                # Update specific counters
                if 'SUID bit set' in issues:
                    self.scanner.scan_stats['suid_files'] += 1
                if 'SGID bit set' in issues:
                    self.scanner.scan_stats['sgid_files'] += 1
                if 'World-writable' in issues or 'Potentially world-writable' in issues:
                    self.scanner.scan_stats['world_writable'] += 1
                if any('writable' in issue for issue in issues):
                    self.scanner.scan_stats['non_owner_writable'] += 1
                
                # Log the finding
                self.logger.warning(f"REAL-TIME ALERT: Unsafe file detected - {file_path}")
                self.logger.warning(f"  Risk Level: {risk_level}")
                self.logger.warning(f"  Issues: {', '.join(issues)}")
                
                # Call callback if provided
                if self.callback:
                    self.callback(unsafe_file)
                    
        except (OSError, PermissionError) as e:
            self.logger.debug(f"Could not check file {file_path}: {e}")
    
    def _should_exclude_file(self, file_path: str) -> bool:
        """Check if file should be excluded from monitoring."""
        path_obj = Path(file_path)
        
        # Check exclude patterns
        for pattern in self.scanner.config.get('exclude_patterns', []):
            if pattern in str(path_obj):
                return True
        
        # Check file size
        try:
            file_size = os.path.getsize(file_path)
            if file_size > self.scanner.config.get('max_file_size', 100 * 1024 * 1024):
                return True
        except OSError:
            pass
        
        return False


class RealTimeMonitor:
    """Real-time file system monitor using watchdog."""
    
    def __init__(self, scanner, callback: Optional[Callable] = None):
        self.scanner = scanner
        self.callback = callback
        self.observer = None
        self.is_monitoring = False
        self.monitored_dirs = []
        self.logger = logging.getLogger(__name__)
        
        if not WATCHDOG_AVAILABLE:
            raise ImportError("watchdog library is required for real-time monitoring. Install with: pip install watchdog")
    
    def start_monitoring(self, directories: List[str]) -> None:
        """Start monitoring specified directories."""
        if self.is_monitoring:
            self.logger.warning("Monitoring is already active")
            return
        
        self.observer = Observer()
        event_handler = UnsafeFileEventHandler(self.scanner, self.callback)
        
        for directory in directories:
            if os.path.exists(directory) and os.path.isdir(directory):
                self.observer.schedule(event_handler, directory, recursive=True)
                self.monitored_dirs.append(directory)
                self.logger.info(f"Started monitoring directory: {directory}")
            else:
                self.logger.warning(f"Directory does not exist or is not accessible: {directory}")
        
        if self.monitored_dirs:
            self.observer.start()
            self.is_monitoring = True
            self.logger.info(f"Real-time monitoring started for {len(self.monitored_dirs)} directories")
        else:
            self.logger.error("No valid directories to monitor")
    
    def stop_monitoring(self) -> None:
        """Stop monitoring."""
        if self.observer and self.is_monitoring:
            self.observer.stop()
            self.observer.join()
            self.is_monitoring = False
            self.logger.info("Real-time monitoring stopped")
    
    def get_status(self) -> Dict:
        """Get monitoring status."""
        return {
            'is_monitoring': self.is_monitoring,
            'monitored_directories': self.monitored_dirs.copy(),
            'watchdog_available': WATCHDOG_AVAILABLE
        }


class RealTimeMonitorGUI:
    """GUI wrapper for real-time monitoring."""
    
    def __init__(self, scanner, gui_callback: Optional[Callable] = None):
        self.scanner = scanner
        self.gui_callback = gui_callback
        self.monitor = None
        self.monitor_thread = None
        self.logger = logging.getLogger(__name__)
    
    def start_monitoring(self, directories: List[str]) -> None:
        """Start monitoring in a separate thread."""
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.logger.warning("Monitoring thread is already running")
            return
        
        def monitor_callback(unsafe_file):
            """Callback for when unsafe files are detected."""
            if self.gui_callback:
                self.gui_callback(unsafe_file)
        
        self.monitor = RealTimeMonitor(self.scanner, monitor_callback)
        self.monitor_thread = threading.Thread(
            target=self.monitor.start_monitoring,
            args=(directories,),
            daemon=True
        )
        self.monitor_thread.start()
    
    def stop_monitoring(self) -> None:
        """Stop monitoring."""
        if self.monitor:
            self.monitor.stop_monitoring()
    
    def get_status(self) -> Dict:
        """Get monitoring status."""
        if self.monitor:
            return self.monitor.get_status()
        return {'is_monitoring': False, 'monitored_directories': [], 'watchdog_available': WATCHDOG_AVAILABLE}


def check_watchdog_availability() -> bool:
    """Check if watchdog library is available."""
    return WATCHDOG_AVAILABLE


def install_watchdog_instructions() -> str:
    """Get instructions for installing watchdog."""
    return """
To enable real-time monitoring, install the watchdog library:

pip install watchdog

Or add it to your requirements.txt:
watchdog>=2.1.0

Then restart the application to enable real-time monitoring features.
"""
