# Installation Guide

## Quick Installation

### Option 1: From GitHub (Recommended)
```bash
git clone https://github.com/yourusername/unsafe-file-scanner.git
cd unsafe-file-scanner
pip install -e .
```

### Option 2: Direct pip Installation
```bash
pip install git+https://github.com/yourusername/unsafe-file-scanner.git
```

### Option 3: Using Installation Scripts
```bash
# Linux/macOS
chmod +x install.sh
./install.sh

# Windows
install.bat
```

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **RAM**: 512 MB
- **Disk Space**: 50 MB

### Recommended Requirements
- **Python**: 3.9 or higher
- **OS**: Windows 11, macOS 12+, or Linux (Ubuntu 20.04+)
- **RAM**: 1 GB
- **Disk Space**: 100 MB

## Platform-Specific Instructions

### Windows

#### Method 1: Using pip
```cmd
pip install git+https://github.com/yourusername/unsafe-file-scanner.git
```

#### Method 2: From Source
```cmd
git clone https://github.com/yourusername/unsafe-file-scanner.git
cd unsafe-file-scanner
pip install -e .
```

#### Method 3: Using Installation Script
```cmd
install.bat
```

### Linux

#### Method 1: Using pip
```bash
pip3 install git+https://github.com/yourusername/unsafe-file-scanner.git
```

#### Method 2: From Source
```bash
git clone https://github.com/yourusername/unsafe-file-scanner.git
cd unsafe-file-scanner
pip3 install -e .
```

#### Method 3: Using Installation Script
```bash
chmod +x install.sh
./install.sh
```

### macOS

#### Method 1: Using pip
```bash
pip3 install git+https://github.com/yourusername/unsafe-file-scanner.git
```

#### Method 2: From Source
```bash
git clone https://github.com/yourusername/unsafe-file-scanner.git
cd unsafe-file-scanner
pip3 install -e .
```

#### Method 3: Using Installation Script
```bash
chmod +x install.sh
./install.sh
```

## Docker Installation

### Build Docker Image
```bash
docker build -t unsafe-file-scanner .
```

### Run with Docker
```bash
# Command line
docker run -v /path/to/scan:/scan unsafe-file-scanner --cli /scan

# GUI (requires X11 forwarding)
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /path/to/scan:/scan unsafe-file-scanner
```

## Usage After Installation

### Command Line Interface
```bash
# Basic scan
unsafe-file-scanner /path/to/scan

# With options
unsafe-file-scanner --output results.json --verbose /path/to/scan

# Short command
ufs /path/to/scan
```

### Graphical User Interface
```bash
# Launch GUI
unsafe-file-scanner-gui

# Short command
ufs-gui
```

## Troubleshooting

### Common Issues

1. **Permission Denied on Linux/macOS**
   ```bash
   chmod +x install.sh
   sudo ./install.sh
   ```

2. **Python Not Found**
   - Install Python 3.8+ from [python.org](https://python.org)
   - Ensure Python is in your PATH

3. **GUI Not Working on Linux**
   ```bash
   # Install GUI dependencies
   sudo apt-get install python3-tk
   # or
   sudo yum install tkinter
   ```

4. **Real-time Monitoring Not Available**
   ```bash
   pip install watchdog
   ```

5. **Import Errors**
   ```bash
   # Reinstall the package
   pip uninstall unsafe-file-scanner
   pip install git+https://github.com/yourusername/unsafe-file-scanner.git
   ```

### Getting Help

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/unsafe-file-scanner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/unsafe-file-scanner/discussions)

## Uninstallation

### Remove Package
```bash
pip uninstall unsafe-file-scanner
```

### Remove Desktop Shortcuts
```bash
# Linux
rm ~/.local/share/applications/unsafe-file-scanner.desktop

# Windows
del "%USERPROFILE%\Desktop\Unsafe File Scanner.lnk"
```

## Development Installation

For developers who want to contribute:

```bash
# Clone repository
git clone https://github.com/yourusername/unsafe-file-scanner.git
cd unsafe-file-scanner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```