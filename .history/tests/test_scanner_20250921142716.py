"""
Tests for the core UnsafeFileScanner functionality
"""

import pytest
import tempfile
import os
import stat
from pathlib import Path
from unsafe_file_scanner import UnsafeFileScanner, UnsafeFile


class TestUnsafeFileScanner:
    """Test cases for UnsafeFileScanner class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.scanner = UnsafeFileScanner()
        self.temp_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_scanner_initialization(self):
        """Test scanner initialization"""
        assert self.scanner is not None
        assert hasattr(self.scanner, 'config')
        assert hasattr(self.scanner, 'unsafe_files')
        assert hasattr(self.scanner, 'scan_stats')
    
    def test_scan_nonexistent_directory(self):
        """Test scanning a non-existent directory"""
        with pytest.raises(FileNotFoundError):
            self.scanner.run_scan(['/nonexistent/directory'])
    
    def test_scan_empty_directory(self):
        """Test scanning an empty directory"""
        result = self.scanner.run_scan([self.temp_dir])
        assert result is not None
        assert self.scanner.scan_stats['total_files'] == 0
        assert self.scanner.scan_stats['unsafe_files'] == 0
    
    def test_scan_with_normal_file(self):
        """Test scanning a directory with normal files"""
        # Create a normal file
        normal_file = os.path.join(self.temp_dir, 'normal_file.txt')
        with open(normal_file, 'w') as f:
            f.write('test content')
        
        result = self.scanner.run_scan([self.temp_dir])
        assert result is not None
        assert self.scanner.scan_stats['total_files'] >= 1
        # Normal file should not be flagged as unsafe
        assert self.scanner.scan_stats['unsafe_files'] == 0
    
    def test_scan_with_world_writable_file(self):
        """Test scanning a world-writable file"""
        # Create a world-writable file
        world_writable_file = os.path.join(self.temp_dir, 'world_writable.txt')
        with open(world_writable_file, 'w') as f:
            f.write('test content')
        
        # Make it world-writable
        os.chmod(world_writable_file, 0o666)
        
        result = self.scanner.run_scan([self.temp_dir])
        assert result is not None
        assert self.scanner.scan_stats['total_files'] >= 1
        assert self.scanner.scan_stats['unsafe_files'] >= 1
        assert self.scanner.scan_stats['world_writable'] >= 1
    
    def test_scan_with_suid_file(self):
        """Test scanning a SUID file"""
        # Create a SUID file
        suid_file = os.path.join(self.temp_dir, 'suid_file')
        with open(suid_file, 'w') as f:
            f.write('#!/bin/bash\necho "test"')
        
        # Make it executable and SUID
        os.chmod(suid_file, 0o4755)
        
        result = self.scanner.run_scan([self.temp_dir])
        assert result is not None
        assert self.scanner.scan_stats['total_files'] >= 1
        assert self.scanner.scan_stats['unsafe_files'] >= 1
        assert self.scanner.scan_stats['suid_files'] >= 1
    
    def test_scan_with_sgid_file(self):
        """Test scanning a SGID file"""
        # Create a SGID file
        sgid_file = os.path.join(self.temp_dir, 'sgid_file')
        with open(sgid_file, 'w') as f:
            f.write('#!/bin/bash\necho "test"')
        
        # Make it executable and SGID
        os.chmod(sgid_file, 0o2755)
        
        result = self.scanner.run_scan([self.temp_dir])
        assert result is not None
        assert self.scanner.scan_stats['total_files'] >= 1
        assert self.scanner.scan_stats['unsafe_files'] >= 1
        assert self.scanner.scan_stats['sgid_files'] >= 1
    
    def test_generate_report(self):
        """Test report generation"""
        # Create a test file
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        self.scanner.run_scan([self.temp_dir])
        report = self.scanner.generate_report()
        
        assert 'metadata' in report
        assert 'statistics' in report
        assert 'files' in report
        assert report['metadata']['total_files_scanned'] >= 1
    
    def test_save_report_json(self):
        """Test saving report in JSON format"""
        # Create a test file
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        self.scanner.run_scan([self.temp_dir])
        report = self.scanner.generate_report()
        
        # Save report
        report_file = os.path.join(self.temp_dir, 'test_report.json')
        self.scanner.save_report(report, report_file)
        
        assert os.path.exists(report_file)
        assert os.path.getsize(report_file) > 0
    
    def test_save_report_csv(self):
        """Test saving report in CSV format"""
        # Create a test file
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        self.scanner.run_scan([self.temp_dir])
        report = self.scanner.generate_report()
        
        # Save report
        report_file = os.path.join(self.temp_dir, 'test_report.csv')
        self.scanner.save_report(report, report_file)
        
        assert os.path.exists(report_file)
        assert os.path.getsize(report_file) > 0
    
    def test_save_report_html(self):
        """Test saving report in HTML format"""
        # Create a test file
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        self.scanner.run_scan([self.temp_dir])
        report = self.scanner.generate_report()
        
        # Save report
        report_file = os.path.join(self.temp_dir, 'test_report.html')
        self.scanner.save_report(report, report_file)
        
        assert os.path.exists(report_file)
        assert os.path.getsize(report_file) > 0


class TestUnsafeFile:
    """Test cases for UnsafeFile class"""
    
    def test_unsafe_file_creation(self):
        """Test UnsafeFile object creation"""
        file_path = "/test/path"
        permissions = "rwxrwxrwx"
        owner = "testuser"
        group = "testgroup"
        size = 1024
        risk_level = "HIGH"
        issues = ["World-writable"]
        
        unsafe_file = UnsafeFile(
            path=file_path,
            permissions=permissions,
            owner=owner,
            group=group,
            size=size,
            risk_level=risk_level,
            issues=issues
        )
        
        assert unsafe_file.path == file_path
        assert unsafe_file.permissions == permissions
        assert unsafe_file.owner == owner
        assert unsafe_file.group == group
        assert unsafe_file.size == size
        assert unsafe_file.risk_level == risk_level
        assert unsafe_file.issues == issues
    
    def test_unsafe_file_to_dict(self):
        """Test UnsafeFile to_dict method"""
        unsafe_file = UnsafeFile(
            path="/test/path",
            permissions="rwxrwxrwx",
            owner="testuser",
            group="testgroup",
            size=1024,
            risk_level="HIGH",
            issues=["World-writable"]
        )
        
        file_dict = unsafe_file.to_dict()
        
        assert isinstance(file_dict, dict)
        assert file_dict['path'] == "/test/path"
        assert file_dict['permissions'] == "rwxrwxrwx"
        assert file_dict['owner'] == "testuser"
        assert file_dict['group'] == "testgroup"
        assert file_dict['size'] == 1024
        assert file_dict['risk_level'] == "HIGH"
        assert file_dict['issues'] == ["World-writable"]


if __name__ == "__main__":
    pytest.main([__file__])
