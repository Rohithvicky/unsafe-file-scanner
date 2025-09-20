#!/usr/bin/env python
"""
Unsafe File Scanner - A Linux Security Tool (Python Version)

This tool scans directories recursively to detect files with unsafe permissions,
including world-writable files, SUID/SGID binaries, and files writable by non-owners.

Author: AI Assistant
Version: 1.0.0
"""

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


@dataclass
class UnsafeFile:
    """Represents an unsafe file with its security issues."""
    path: str
    permissions: str
    owner: str
    group: str
    size: int
    modified_time: str
    issues: List[str]
    risk_level: str


class UnsafeFileScanner:
    """Main scanner class for detecting unsafe file permissions."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize the scanner with optional configuration."""
        self.config = self._load_config(config_file)
        self.setup_logging()
        self.unsafe_files: List[UnsafeFile] = []
        self.scan_stats = {
            'total_files': 0,
            'unsafe_files': 0,
            'suid_files': 0,
            'sgid_files': 0,
            'world_writable': 0,
            'non_owner_writable': 0,
            'scan_duration': 0
        }
    
    def _load_config(self, config_file: Optional[str]) -> Dict:
        """Load configuration from file or use defaults."""
        default_config = {
            'exclude_dirs': ['.git', '.svn', 'node_modules', '__pycache__', '.pytest_cache'],
            'exclude_files': ['.DS_Store', 'Thumbs.db'],
            'max_file_size': 100 * 1024 * 1024,  # 100MB
            'follow_symlinks': False,
            'log_level': 'INFO',
            'output_format': 'json',
            'output_file': None,
            'risk_thresholds': {
                'high': ['suid', 'sgid', 'world_writable'],
                'medium': ['non_owner_writable'],
                'low': ['other_issues']
            }
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config file {config_file}: {e}")
                print("Using default configuration.")
        
        return default_config
    
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
    
    def is_excluded(self, path: str) -> bool:
        """Check if a path should be excluded from scanning."""
        path_obj = Path(path)
        
        # Check if any parent directory is in exclude list
        for part in path_obj.parts:
            if part in self.config['exclude_dirs']:
                return True
        
        # Check if file itself should be excluded
        if path_obj.name in self.config['exclude_files']:
            return True
        
        return False
    
    def get_file_permissions(self, file_path: str) -> Tuple[str, str, str, str]:
        """Get file permissions, owner, and group information."""
        try:
            stat_info = os.stat(file_path, follow_symlinks=self.config['follow_symlinks'])
            
            # Get permission string (e.g., 'rwxr-xr-x')
            permissions = stat.filemode(stat_info.st_mode)
            
            # Get owner and group names
            if UNIX_PLATFORM and pwd and grp:
                try:
                    owner = pwd.getpwuid(stat_info.st_uid).pw_name
                except KeyError:
                    owner = str(stat_info.st_uid)
                
                try:
                    group = grp.getgrgid(stat_info.st_gid).gr_name
                except KeyError:
                    group = str(stat_info.st_gid)
            else:
                # Windows or other non-Unix platform
                owner = str(stat_info.st_uid)
                group = str(stat_info.st_gid)
            
            # Get file size
            size = stat_info.st_size
            
            return permissions, owner, group, size
            
        except (OSError, PermissionError) as e:
            self.logger.warning(f"Could not access {file_path}: {e}")
            return "unknown", "unknown", "unknown", 0
    
    def check_suid_sgid(self, file_path: str, stat_info: os.stat_result) -> List[str]:
        """Check for SUID and SGID bits."""
        issues = []
        
        # SUID/SGID are Unix concepts, skip on Windows
        if not UNIX_PLATFORM:
            return issues
            
        mode = stat_info.st_mode
        
        if mode & stat.S_ISUID:
            issues.append("SUID bit set")
        
        if mode & stat.S_ISGID:
            issues.append("SGID bit set")
        
        return issues
    
    def check_world_writable(self, file_path: str, stat_info: os.stat_result) -> List[str]:
        """Check if file is world-writable."""
        issues = []
        
        # World-writable is a Unix concept, adapt for Windows
        if not UNIX_PLATFORM:
            # On Windows, check if file is writable by everyone
            # This is a simplified check - Windows permissions are more complex
            try:
                # Try to open file for writing
                with open(file_path, 'a'):
                    pass
                # If we can write, check if it's in a public location
                if any(public in file_path.lower() for public in ['public', 'shared', 'temp', 'tmp']):
                    issues.append("Potentially world-writable (Windows)")
            except (OSError, PermissionError):
                pass
            return issues
            
        mode = stat_info.st_mode
        
        if mode & stat.S_IWOTH:  # World write permission
            issues.append("World-writable")
        
        return issues
    
    def check_non_owner_writable(self, file_path: str, stat_info: os.stat_result) -> List[str]:
        """Check if file is writable by non-owners."""
        issues = []
        
        # Non-owner writable is a Unix concept, adapt for Windows
        if not UNIX_PLATFORM:
            # On Windows, this is more complex due to ACLs
            # For now, we'll skip this check on Windows
            return issues
            
        mode = stat_info.st_mode
        
        # Check if group has write permission but owner doesn't
        if mode & stat.S_IWGRP and not (mode & stat.S_IWUSR):
            issues.append("Group-writable but not owner-writable")
        
        # Check if others have write permission but owner doesn't
        if mode & stat.S_IWOTH and not (mode & stat.S_IWUSR):
            issues.append("Others-writable but not owner-writable")
        
        return issues
    
    def check_other_permissions(self, file_path: str, stat_info: os.stat_result) -> List[str]:
        """Check for other permission-related issues."""
        issues = []
        
        # Permission checks are Unix-specific, adapt for Windows
        if not UNIX_PLATFORM:
            # On Windows, check for some basic issues
            try:
                # Check if file is executable but not readable
                if file_path.endswith(('.exe', '.bat', '.cmd', '.com')):
                    try:
                        with open(file_path, 'r'):
                            pass
                    except (OSError, PermissionError):
                        issues.append("Executable but not readable (Windows)")
            except:
                pass
            return issues
            
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
    
    def assess_risk_level(self, issues: List[str]) -> str:
        """Assess the risk level based on detected issues."""
        high_risk_indicators = self.config['risk_thresholds']['high']
        medium_risk_indicators = self.config['risk_thresholds']['medium']
        
        for issue in issues:
            if any(indicator in issue.lower() for indicator in high_risk_indicators):
                return "HIGH"
            if any(indicator in issue.lower() for indicator in medium_risk_indicators):
                return "MEDIUM"
        
        return "LOW"
    
    def scan_file(self, file_path: str) -> Optional[UnsafeFile]:
        """Scan a single file for unsafe permissions."""
        try:
            if self.is_excluded(file_path):
                return None
            
            # Check file size limit
            if os.path.getsize(file_path) > self.config['max_file_size']:
                self.logger.debug(f"Skipping large file: {file_path}")
                return None
            
            stat_info = os.stat(file_path, follow_symlinks=self.config['follow_symlinks'])
            permissions, owner, group, size = self.get_file_permissions(file_path)
            
            # Check for various permission issues
            all_issues = []
            all_issues.extend(self.check_suid_sgid(file_path, stat_info))
            all_issues.extend(self.check_world_writable(file_path, stat_info))
            all_issues.extend(self.check_non_owner_writable(file_path, stat_info))
            all_issues.extend(self.check_other_permissions(file_path, stat_info))
            
            if not all_issues:
                return None
            
            # Create unsafe file record
            risk_level = self.assess_risk_level(all_issues)
            modified_time = datetime.fromtimestamp(stat_info.st_mtime).isoformat()
            
            unsafe_file = UnsafeFile(
                path=file_path,
                permissions=permissions,
                owner=owner,
                group=group,
                size=size,
                modified_time=modified_time,
                issues=all_issues,
                risk_level=risk_level
            )
            
            # Update statistics
            self.scan_stats['unsafe_files'] += 1
            if "SUID" in all_issues:
                self.scan_stats['suid_files'] += 1
            if "SGID" in all_issues:
                self.scan_stats['sgid_files'] += 1
            if "World-writable" in all_issues:
                self.scan_stats['world_writable'] += 1
            if any("writable" in issue for issue in all_issues):
                self.scan_stats['non_owner_writable'] += 1
            
            return unsafe_file
            
        except (OSError, PermissionError) as e:
            self.logger.warning(f"Error scanning {file_path}: {e}")
            return None
    
    def scan_directory(self, directory: str) -> None:
        """Recursively scan a directory for unsafe files."""
        self.logger.info(f"Scanning directory: {directory}")
        
        try:
            for root, dirs, files in os.walk(directory, followlinks=self.config['follow_symlinks']):
                # Remove excluded directories from dirs list to prevent walking into them
                dirs[:] = [d for d in dirs if not self.is_excluded(os.path.join(root, d))]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    self.scan_stats['total_files'] += 1
                    
                    unsafe_file = self.scan_file(file_path)
                    if unsafe_file:
                        self.unsafe_files.append(unsafe_file)
                        self.logger.debug(f"Found unsafe file: {file_path} - {unsafe_file.issues}")
        
        except PermissionError as e:
            self.logger.error(f"Permission denied accessing {directory}: {e}")
        except Exception as e:
            self.logger.error(f"Error scanning {directory}: {e}")
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive scan report."""
        report = {
            'scan_info': {
                'timestamp': datetime.now().isoformat(),
                'scanner_version': '1.0.0',
                'total_files_scanned': self.scan_stats['total_files'],
                'scan_duration_seconds': self.scan_stats['scan_duration']
            },
            'statistics': self.scan_stats,
            'unsafe_files': [asdict(file) for file in self.unsafe_files],
            'summary': {
                'total_unsafe_files': len(self.unsafe_files),
                'high_risk_files': len([f for f in self.unsafe_files if f.risk_level == 'HIGH']),
                'medium_risk_files': len([f for f in self.unsafe_files if f.risk_level == 'MEDIUM']),
                'low_risk_files': len([f for f in self.unsafe_files if f.risk_level == 'LOW'])
            }
        }
        return report
    
    def save_report(self, report: Dict, output_file: str) -> None:
        """Save the scan report to a file."""
        try:
            file_ext = Path(output_file).suffix.lower()
            
            if file_ext == '.csv':
                self._save_csv_report(report, output_file)
            elif file_ext == '.html':
                self._save_html_report(report, output_file)
            else:
                # Default to JSON
                with open(output_file, 'w') as f:
                    json.dump(report, f, indent=2)
            
            self.logger.info(f"Report saved to: {output_file}")
        except Exception as e:
            self.logger.error(f"Error saving report to {output_file}: {e}")
    
    def _save_csv_report(self, report: Dict, output_file: str) -> None:
        """Save report in CSV format."""
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow([
                'File Path', 'Permissions', 'Owner', 'Group', 'Size (bytes)', 
                'Modified Time', 'Risk Level', 'Issues'
            ])
            
            # Write scan summary
            writer.writerow([])
            writer.writerow(['SCAN SUMMARY'])
            writer.writerow(['Total Files Scanned', report['summary']['total_files']])
            writer.writerow(['Unsafe Files Found', report['summary']['total_unsafe_files']])
            writer.writerow(['High Risk Files', report['summary']['high_risk_files']])
            writer.writerow(['Medium Risk Files', report['summary']['medium_risk_files']])
            writer.writerow(['Low Risk Files', report['summary']['low_risk_files']])
            writer.writerow(['Scan Duration (seconds)', report['summary']['scan_duration']])
            writer.writerow([])
            writer.writerow(['DETAILED RESULTS'])
            
            # Write unsafe files
            for file_info in report['unsafe_files']:
                writer.writerow([
                    file_info['path'],
                    file_info['permissions'],
                    file_info['owner'],
                    file_info['group'],
                    file_info['size'],
                    file_info['modified_time'],
                    file_info['risk_level'],
                    '; '.join(file_info['issues'])
                ])
    
    def _save_html_report(self, report: Dict, output_file: str) -> None:
        """Save report in HTML format."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unsafe File Scanner Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 20px; margin-bottom: 30px; }}
        .summary {{ background: #ecf0f1; padding: 20px; border-radius: 5px; margin-bottom: 30px; }}
        .summary h2 {{ color: #2c3e50; margin-top: 0; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: white; padding: 15px; border-radius: 5px; text-align: center; border-left: 4px solid #3498db; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ color: #7f8c8d; margin-top: 5px; }}
        .results {{ margin-top: 30px; }}
        .results h2 {{ color: #2c3e50; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #3498db; color: white; font-weight: bold; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .risk-high {{ color: #e74c3c; font-weight: bold; }}
        .risk-medium {{ color: #f39c12; font-weight: bold; }}
        .risk-low {{ color: #27ae60; font-weight: bold; }}
        .issues {{ max-width: 300px; word-wrap: break-word; }}
        .footer {{ text-align: center; margin-top: 40px; color: #7f8c8d; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Unsafe File Scanner Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <h2>📊 Scan Summary</h2>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{report['summary']['total_files']}</div>
                    <div class="stat-label">Total Files Scanned</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{report['summary']['total_unsafe_files']}</div>
                    <div class="stat-label">Unsafe Files Found</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{report['summary']['high_risk_files']}</div>
                    <div class="stat-label">High Risk</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{report['summary']['medium_risk_files']}</div>
                    <div class="stat-label">Medium Risk</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{report['summary']['low_risk_files']}</div>
                    <div class="stat-label">Low Risk</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{report['summary']['scan_duration']:.2f}s</div>
                    <div class="stat-label">Scan Duration</div>
                </div>
            </div>
        </div>
        
        <div class="results">
            <h2>🔍 Detailed Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>File Path</th>
                        <th>Permissions</th>
                        <th>Owner</th>
                        <th>Group</th>
                        <th>Size</th>
                        <th>Risk Level</th>
                        <th>Issues</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Add unsafe files to HTML
        for file_info in report['unsafe_files']:
            risk_class = f"risk-{file_info['risk_level'].lower()}"
            html_content += f"""
                    <tr>
                        <td><code>{file_info['path']}</code></td>
                        <td><code>{file_info['permissions']}</code></td>
                        <td>{file_info['owner']}</td>
                        <td>{file_info['group']}</td>
                        <td>{file_info['size']:,} bytes</td>
                        <td class="{risk_class}">{file_info['risk_level']}</td>
                        <td class="issues">{'; '.join(file_info['issues'])}</td>
                    </tr>
"""
        
        html_content += """
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Generated by Unsafe File Scanner - A Linux Security Tool</p>
            <p>For more information, visit the project documentation</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def print_summary(self) -> None:
        """Print a summary of the scan results."""
        print("\n" + "="*60)
        print("UNSAFE FILE SCANNER - SCAN SUMMARY")
        print("="*60)
        print(f"Total files scanned: {self.scan_stats['total_files']}")
        print(f"Unsafe files found: {self.scan_stats['unsafe_files']}")
        print(f"SUID files: {self.scan_stats['suid_files']}")
        print(f"SGID files: {self.scan_stats['sgid_files']}")
        print(f"World-writable files: {self.scan_stats['world_writable']}")
        print(f"Non-owner writable files: {self.scan_stats['non_owner_writable']}")
        print(f"Scan duration: {self.scan_stats['scan_duration']:.2f} seconds")
        
        if self.unsafe_files:
            print(f"\nRisk Level Breakdown:")
            high_risk = len([f for f in self.unsafe_files if f.risk_level == 'HIGH'])
            medium_risk = len([f for f in self.unsafe_files if f.risk_level == 'MEDIUM'])
            low_risk = len([f for f in self.unsafe_files if f.risk_level == 'LOW'])
            print(f"  HIGH: {high_risk}")
            print(f"  MEDIUM: {medium_risk}")
            print(f"  LOW: {low_risk}")
        
        print("="*60)
    
    def run_scan(self, directories: List[str]) -> None:
        """Run the complete scan on specified directories."""
        start_time = time.time()
        
        self.logger.info("Starting unsafe file scan...")
        self.logger.info(f"Target directories: {directories}")
        
        for directory in directories:
            if not os.path.exists(directory):
                self.logger.error(f"Directory does not exist: {directory}")
                continue
            
            if not os.path.isdir(directory):
                self.logger.error(f"Path is not a directory: {directory}")
                continue
            
            self.scan_directory(directory)
        
        self.scan_stats['scan_duration'] = time.time() - start_time
        
        # Generate and save report
        report = self.generate_report()
        
        if self.config['output_file']:
            self.save_report(report, self.config['output_file'])
        
        # Print summary
        self.print_summary()
        
        # Print detailed results if requested
        if self.unsafe_files and self.config.get('verbose', False):
            print(f"\nDetailed Results:")
            print("-" * 60)
            for file in self.unsafe_files:
                print(f"File: {file.path}")
                print(f"  Permissions: {file.permissions}")
                print(f"  Owner: {file.owner}, Group: {file.group}")
                print(f"  Risk Level: {file.risk_level}")
                print(f"  Issues: {', '.join(file.issues)}")
                print()


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Unsafe File Scanner - A Linux Security Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python unsafe_file_scanner.py /etc /bin /usr/bin
  python unsafe_file_scanner.py --config config.json /home/user
  python unsafe_file_scanner.py --output report.json --verbose /var
        """
    )
    
    parser.add_argument(
        'directories',
        nargs='+',
        help='Directories to scan for unsafe files'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Configuration file path'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file for scan report (JSON format)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set logging level'
    )
    
    args = parser.parse_args()
    
    # Initialize scanner
    scanner = UnsafeFileScanner(args.config)
    
    # Override config with command line arguments
    if args.output:
        scanner.config['output_file'] = args.output
    if args.verbose:
        scanner.config['verbose'] = True
    if args.log_level:
        scanner.config['log_level'] = args.log_level
        scanner.setup_logging()
    
    try:
        # Run the scan
        scanner.run_scan(args.directories)
        
        # Exit with appropriate code
        if scanner.unsafe_files:
            sys.exit(1)  # Found unsafe files
        else:
            sys.exit(0)  # No unsafe files found
            
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error during scan: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
