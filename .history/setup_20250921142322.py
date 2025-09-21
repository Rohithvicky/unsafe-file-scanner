#!/usr/bin/env python3
"""
Setup script for Unsafe File Scanner
Professional Security Tool for File Permission Analysis
"""

from setuptools import setup, find_packages
import os
import sys

# Ensure we're using Python 3.8+
if sys.version_info < (3, 8):
    sys.exit("Unsafe File Scanner requires Python 3.8 or higher")

# Read the README file
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Professional Security Tool for File Permission Analysis"

# Read requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [
                line.strip() 
                for line in fh 
                if line.strip() 
                and not line.startswith("#") 
                and not line.startswith("tkinter")  # Built-in module
            ]
    except FileNotFoundError:
        return ["watchdog>=2.1.0"]

# Read version from __init__.py
def get_version():
    try:
        with open("unsafe_file_scanner/__init__.py", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return "1.0.0"

setup(
    name="unsafe-file-scanner",
    version=get_version(),
    author="Rohith Vicky",
    author_email="rohithvicky@example.com",
    maintainer="Rohith Vicky",
    maintainer_email="rohithvicky@example.com",
    description="Professional Security Tool for File Permission Analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Rohithvicky/unsafe-file-scanner",
    download_url="https://github.com/Rohithvicky/unsafe-file-scanner/archive/v1.0.0.tar.gz",
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    classifiers=[
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
        "unsafe_file_scanner": [
            "*.json", 
            "*.md", 
            "*.txt",
            "*.yml",
            "*.yaml"
        ],
    },
    data_files=[
        ("share/unsafe-file-scanner", [
            "README.md",
            "LICENSE",
            "CHANGELOG.md",
            "INSTALLATION.md",
            "CONTRIBUTING.md",
            "PROJECT_OVERVIEW.md",
        ]),
    ],
    keywords=[
        "security", 
        "file-permissions", 
        "linux", 
        "suid", 
        "sgid", 
        "world-writable", 
        "privilege-escalation", 
        "file-integrity", 
        "monitoring",
        "file-system",
        "permission-analysis",
        "security-audit",
        "system-administration",
        "gui",
        "cli",
        "real-time-monitoring"
    ],
    project_urls={
        "Homepage": "https://github.com/Rohithvicky/unsafe-file-scanner",
        "Bug Reports": "https://github.com/Rohithvicky/unsafe-file-scanner/issues",
        "Source": "https://github.com/Rohithvicky/unsafe-file-scanner",
        "Documentation": "https://github.com/Rohithvicky/unsafe-file-scanner/wiki",
        "Download": "https://github.com/Rohithvicky/unsafe-file-scanner/releases",
        "Changelog": "https://github.com/Rohithvicky/unsafe-file-scanner/blob/main/CHANGELOG.md",
    },
    zip_safe=False,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "pytest-xdist>=3.3.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
            "bandit>=1.7.0",
            "safety>=2.3.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "sphinx-autodoc-typehints>=1.23.0",
        ],
        "build": [
            "build>=0.10.0",
            "twine>=4.0.0",
            "wheel>=0.40.0",
        ],
    },
    options={
        "bdist_wheel": {
            "universal": False,
        },
    },
    platforms=["Linux", "Windows", "macOS"],
    license="MIT",
    copyright="Copyright (c) 2024 Rohith Vicky",
)
