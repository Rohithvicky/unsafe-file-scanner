#!/bin/bash
# Professional Installation Script for Unsafe File Scanner
# Supports Linux and macOS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get Python version
get_python_version() {
    python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0"
}

# Function to check if version meets requirement
version_meets_requirement() {
    local required="$1"
    local current="$2"
    [ "$(printf '%s\n' "$required" "$current" | sort -V | head -n1)" = "$required" ]
}

# Main installation function
main() {
    echo "🔒 Unsafe File Scanner - Professional Installation Script"
    echo "========================================================="
    echo ""

    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root. Consider using a virtual environment."
    fi

    # Check if Python 3 is installed
    if ! command_exists python3; then
        print_error "Python 3 is not installed."
        echo ""
        echo "Please install Python 3.8 or higher:"
        echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
        echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
        echo "  macOS:         brew install python3"
        echo "  Or download from: https://www.python.org/downloads/"
        exit 1
    fi

    # Check Python version
    PYTHON_VERSION=$(get_python_version)
    REQUIRED_VERSION="3.8"

    if ! version_meets_requirement "$REQUIRED_VERSION" "$PYTHON_VERSION"; then
        print_error "Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
        echo ""
        echo "Please upgrade Python:"
        echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3.8"
        echo "  CentOS/RHEL:   sudo yum install python3.8"
        echo "  macOS:         brew install python3"
        exit 1
    fi

    print_success "Python $PYTHON_VERSION found"

    # Check if pip is installed
    if ! command_exists pip3; then
        print_error "pip3 is not installed."
        echo ""
        echo "Please install pip3:"
        echo "  Ubuntu/Debian: sudo apt install python3-pip"
        echo "  CentOS/RHEL:   sudo yum install python3-pip"
        echo "  macOS:         python3 -m ensurepip --upgrade"
        exit 1
    fi

    print_success "pip3 found"

    # Check if we're in the right directory
    if [ ! -f "setup.py" ] || [ ! -f "requirements.txt" ]; then
        print_error "setup.py or requirements.txt not found."
        echo "Please run this script from the Unsafe File Scanner root directory."
        exit 1
    fi

    # Create virtual environment (optional but recommended)
    if [ "$1" = "--venv" ] || [ "$1" = "-v" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        print_success "Virtual environment created and activated"
    fi

    # Upgrade pip
    print_status "Upgrading pip..."
    pip3 install --upgrade pip

    # Install dependencies
    print_status "Installing dependencies..."
    pip3 install -r requirements.txt

    # Install the package
    print_status "Installing Unsafe File Scanner..."
    pip3 install -e .

    if [ $? -eq 0 ]; then
        print_success "Installation completed successfully!"
        echo ""
        echo "🚀 Usage Examples:"
        echo "  Command Line: unsafe-file-scanner /path/to/scan"
        echo "  GUI:          unsafe-file-scanner-gui"
        echo "  Short CLI:    ufs /path/to/scan"
        echo "  Short GUI:    ufs-gui"
        echo ""
        echo "📖 Documentation:"
        echo "  README:       cat README.md"
        echo "  Help:         unsafe-file-scanner --help"
        echo ""
        echo "🔧 Development:"
        echo "  Install dev:  pip install -r requirements-dev.txt"
        echo "  Run tests:    pytest"
        echo ""
        
        # Check if GUI is available
        if python3 -c "import tkinter" 2>/dev/null; then
            print_success "GUI support available"
        else
            print_warning "GUI support not available (tkinter not found)"
            echo "  Install GUI: sudo apt install python3-tk (Ubuntu/Debian)"
        fi

        # Check if watchdog is available
        if python3 -c "import watchdog" 2>/dev/null; then
            print_success "Real-time monitoring available"
        else
            print_warning "Real-time monitoring not available (watchdog not installed)"
        fi

        # Create desktop shortcut (Linux)
        if [ "$XDG_CURRENT_DESKTOP" ] && [ -d "$HOME/.local/share/applications" ]; then
            print_status "Creating desktop shortcut..."
            cat > ~/.local/share/applications/unsafe-file-scanner.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Unsafe File Scanner
Comment=Professional Security Analysis & File Permission Monitoring
Exec=unsafe-file-scanner-gui
Icon=security-high
Terminal=false
Categories=Security;System;
Keywords=security;file;permission;monitor;
EOF
            chmod +x ~/.local/share/applications/unsafe-file-scanner.desktop
            print_success "Desktop shortcut created"
        fi

    else
        print_error "Installation failed!"
        exit 1
    fi
}

# Show help
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --venv, -v     Create and use virtual environment"
    echo "  --help, -h     Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0              # Install system-wide"
    echo "  $0 --venv       # Install in virtual environment"
    exit 0
fi

# Run main function
main "$@"