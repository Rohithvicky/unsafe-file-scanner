# Unsafe File Scanner - Project Overview

## 🎯 Project Summary

**Unsafe File Scanner** is a professional security tool designed to detect files with unsafe permissions and potential security vulnerabilities. It provides comprehensive file system security analysis with both command-line and graphical interfaces, making it suitable for security professionals, system administrators, and developers.

## 🏗️ Project Structure

```
unsafe-file-scanner/
├── unsafe_file_scanner/           # Main package directory
│   ├── __init__.py               # Package initialization
│   ├── unsafe_file_scanner.py    # Core scanner logic
│   ├── unsafe_file_scanner_gui.py # GUI interface
│   ├── realtime_monitor.py       # Real-time monitoring
│   └── rule_engine.py            # Rule engine for custom checks
├── .github/                      # GitHub configuration
│   └── workflows/
│       └── ci.yml               # CI/CD pipeline
├── main.py                       # Main entry point
├── setup.py                      # Package setup script
├── requirements.txt              # Python dependencies
├── README.md                     # Main documentation
├── INSTALLATION.md               # Installation guide
├── CONTRIBUTING.md               # Contribution guidelines
├── CHANGELOG.md                  # Version history
├── LICENSE                       # MIT License
├── .gitignore                    # Git ignore rules
├── Dockerfile                    # Docker configuration
├── install.sh                    # Linux/macOS installation script
├── install.bat                   # Windows installation script
├── config.json                   # Default configuration
└── advanced_config.json          # Advanced configuration
```

## ✨ Key Features

### 🔍 **Core Security Analysis**
- **SUID/SGID Detection**: Identifies files with Set User ID and Set Group ID permissions
- **World-Writable Files**: Detects files writable by all users (major security risk)
- **Non-Owner Writable Files**: Finds files writable by users other than the owner
- **Permission Risk Assessment**: Categorizes files by risk levels (CRITICAL, HIGH, MEDIUM, LOW)

### 🖥️ **Professional GUI Interface**
- **Modern Design**: Clean, intuitive two-panel layout
- **Real-time Status**: Live progress tracking and status indicators
- **Tabbed Results**: Summary, detailed results, and raw JSON views
- **Advanced Controls**: Real-time monitoring and rule management

### ⚡ **Real-time Monitoring**
- **Live Detection**: Uses `watchdog` library for real-time file system monitoring
- **Alert System**: Instant notifications for security threats
- **Result Management**: View, export, and manage accumulated results

### 🛡️ **Advanced Security Features**
- **Customizable Rule Engine**: 15+ built-in security rules with custom rule support
- **Multi-format Export**: JSON, CSV, and HTML report generation
- **Cross-platform Support**: Works on Windows, Linux, and macOS
- **Professional Logging**: Comprehensive audit trails

## 🚀 Installation & Usage

### Quick Installation
```bash
# From GitHub
git clone https://github.com/Rohithvicky/unsafe-file-scanner.git
cd unsafe-file-scanner
pip install -e .

# Direct pip installation
pip install git+https://github.com/Rohithvicky/unsafe-file-scanner.git
```

### Usage
```bash
# Command line
unsafe-file-scanner /path/to/scan
ufs /path/to/scan

# GUI
unsafe-file-scanner-gui
ufs-gui
```

## 🔧 Technical Implementation

### **Core Technologies**
- **Python 3.8+**: Main programming language
- **tkinter**: GUI framework
- **watchdog**: Real-time file system monitoring
- **os/stat**: File system operations and permission analysis
- **Bitwise Operations**: Advanced permission bit analysis

### **Architecture**
- **Modular Design**: Separate modules for different functionalities
- **Cross-platform**: Platform-specific adaptations for Windows, Linux, macOS
- **Threading**: Non-blocking GUI operations
- **Configuration Management**: JSON-based configuration system
- **Error Handling**: Comprehensive error handling and user feedback

### **Security Features**
- **Permission Analysis**: Deep analysis of file permissions and security risks
- **Real-time Monitoring**: Live detection of security threats
- **Rule Engine**: Customizable security rules for advanced threat detection
- **Risk Assessment**: Automated risk level categorization
- **Audit Trails**: Comprehensive logging and reporting

## 📊 Export & Reporting

### **Supported Formats**
- **JSON**: Structured data format with complete scan details
- **CSV**: Spreadsheet-compatible format for analysis
- **HTML**: Web-friendly formatted reports with styling

### **Report Contents**
- **Scan Summary**: Total files, unsafe files, scan duration
- **File Details**: Path, permissions, owner, group, risk level, issues
- **Risk Breakdown**: Count by risk level (CRITICAL, HIGH, MEDIUM, LOW)
- **Statistics**: Comprehensive scan statistics and metrics

## 🌐 Cross-Platform Support

| Platform | Status | Features |
|----------|--------|----------|
| **Windows** | ✅ Full Support | GUI, CLI, Real-time monitoring |
| **Linux** | ✅ Full Support | All features, native compatibility |
| **macOS** | ✅ Full Support | Native GUI, full functionality |

## 🛠️ Development & Contributing

### **Development Setup**
```bash
git clone https://github.com/Rohithvicky/unsafe-file-scanner.git
cd unsafe-file-scanner
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
pip install -r requirements-dev.txt
```

### **Testing**
```bash
pytest                    # Run all tests
pytest --cov            # Run with coverage
python -m pytest tests/ # Run specific tests
```

### **Code Quality**
- **PEP 8**: Python code style compliance
- **Type Hints**: Comprehensive type annotations
- **Docstrings**: Google-style documentation
- **Linting**: flake8 and mypy validation
- **Formatting**: black code formatting

## 📈 Performance & Scalability

### **Performance Features**
- **Fast Scanning**: Optimized algorithms for large directory trees
- **Memory Efficient**: Streams large files without loading into memory
- **Real-time Monitoring**: Low-latency file system event detection
- **Concurrent Processing**: Multi-threaded scanning for better performance

### **Scalability**
- **Large Directories**: Handles directories with thousands of files
- **Memory Management**: Efficient memory usage for large scans
- **Progress Tracking**: Real-time progress updates for long scans
- **Configurable Limits**: Adjustable file size and scan limits

## 🔒 Security & Compliance

### **Security Features**
- **Permission Analysis**: Comprehensive file permission security analysis
- **Threat Detection**: Real-time detection of security threats
- **Risk Assessment**: Automated risk level categorization
- **Audit Trails**: Complete logging and audit capabilities

### **Compliance**
- **Security Standards**: Aligns with security best practices
- **Audit Support**: Comprehensive reporting for security audits
- **Documentation**: Complete documentation for compliance
- **Open Source**: MIT license for transparency and security

## 🎯 Target Users

### **Primary Users**
- **Security Professionals**: File system security analysis and monitoring
- **System Administrators**: System security auditing and maintenance
- **Developers**: Security testing and vulnerability detection
- **IT Professionals**: Security assessment and compliance checking

### **Use Cases**
- **Security Audits**: Comprehensive file system security analysis
- **Vulnerability Detection**: Identification of security risks and threats
- **Real-time Monitoring**: Live security monitoring and alerting
- **Compliance Checking**: Security compliance verification
- **Research & Analysis**: Security research and threat analysis

## 🚀 Future Roadmap

### **Planned Features**
- **Web Interface**: Browser-based interface for remote monitoring
- **API Support**: REST API for integration with other tools
- **Cloud Integration**: Cloud storage and monitoring support
- **Advanced Analytics**: Machine learning-based threat detection
- **Mobile App**: Mobile interface for monitoring and alerts

### **Enhancement Areas**
- **Performance**: Further optimization for large-scale deployments
- **Security**: Additional security features and threat detection
- **Integration**: Better integration with existing security tools
- **Documentation**: Enhanced documentation and tutorials
- **Community**: Growing community and ecosystem

## 📞 Support & Community

### **Getting Help**
- **Documentation**: Comprehensive user and developer documentation
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Community discussions and support
- **Contributing**: Guidelines for contributing to the project

### **Community**
- **Open Source**: MIT license for community contribution
- **Contributing**: Guidelines for code and documentation contributions
- **Feedback**: Community feedback and feature requests
- **Support**: Community-driven support and assistance

---

**Unsafe File Scanner** - Professional Security Tool for File Permission Analysis

*Made with ❤️ for the security community*
