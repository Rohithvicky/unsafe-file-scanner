#!/usr/bin/env python3
"""
Setup script for Unsafe File Scanner
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="unsafe-file-scanner",
    version="1.0.0",
    author="AI Assistant",
    author_email="assistant@example.com",
    description="Professional Security Tool for File Permission Analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Rohithvicky/unsafe-file-scanner",
    packages=find_packages(),
    classifiers=[
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
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "unsafe-file-scanner=unsafe_file_scanner.unsafe_file_scanner:main",
            "ufs=unsafe_file_scanner.unsafe_file_scanner:main",
            "unsafe-file-scanner-gui=unsafe_file_scanner.unsafe_file_scanner_gui:main",
            "ufs-gui=unsafe_file_scanner.unsafe_file_scanner_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "unsafe_file_scanner": ["*.json", "*.md", "*.txt"],
    },
    keywords="security, file-permissions, linux, suid, sgid, world-writable, privilege-escalation, file-integrity, monitoring",
    project_urls={
        "Bug Reports": "https://github.com/Rohithvicky/unsafe-file-scanner/issues",
        "Source": "https://github.com/Rohithvicky/unsafe-file-scanner",
        "Documentation": "https://github.com/Rohithvicky/unsafe-file-scanner/wiki",
        "Download": "https://github.com/Rohithvicky/unsafe-file-scanner/archive/v1.0.0.tar.gz",
    },
    zip_safe=False,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
        ],
    },
)
