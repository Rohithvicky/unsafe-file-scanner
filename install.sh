#!/bin/bash
# Installation script for Unsafe File Scanner

echo "🔒 Installing Unsafe File Scanner..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Install the package
echo "📦 Installing package..."
pip3 install -e .

# Create desktop shortcut (Linux)
if [ "$XDG_CURRENT_DESKTOP" ]; then
    echo "🖥️ Creating desktop shortcut..."
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
EOF
    chmod +x ~/.local/share/applications/unsafe-file-scanner.desktop
    echo "✅ Desktop shortcut created"
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "Usage:"
echo "  Command Line: unsafe-file-scanner"
echo "  GUI:          unsafe-file-scanner-gui"
echo "  Short:        ufs-gui"
echo ""
echo "For more information, visit: https://github.com/yourusername/unsafe-file-scanner"
