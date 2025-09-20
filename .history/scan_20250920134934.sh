#!/bin/bash
# Unsafe File Scanner - Quick Scan Script
# This script provides easy execution of the unsafe file scanner

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default directories to scan
DEFAULT_DIRS=("/etc" "/bin" "/usr/bin" "/sbin" "/usr/sbin")

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

# Function to show usage
show_usage() {
    echo "Unsafe File Scanner - Quick Scan Script"
    echo "Usage: $0 [OPTIONS] [DIRECTORIES...]"
    echo ""
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -c, --config FILE       Use custom configuration file"
    echo "  -o, --output FILE       Save report to file"
    echo "  -v, --verbose           Enable verbose output"
    echo "  -q, --quick             Quick scan (common directories only)"
    echo "  -f, --full              Full system scan (requires root)"
    echo "  --test                  Run test scan with sample files"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Scan default directories"
    echo "  $0 -q                                 # Quick scan"
    echo "  $0 -f                                 # Full system scan"
    echo "  $0 /home/user /var/log               # Scan specific directories"
    echo "  $0 -c config.json -o report.json     # Use custom config and output"
    echo "  $0 --test                             # Run test scan"
}

# Function to check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root. This may scan system-protected files."
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Exiting..."
            exit 1
        fi
    fi
}

# Function to run test scan
run_test() {
    print_status "Running test scan with sample files..."
    python3 test_scanner.py
    exit $?
}

# Function to run quick scan
run_quick_scan() {
    print_status "Running quick scan on common directories..."
    python3 unsafe_file_scanner.py --verbose "${DEFAULT_DIRS[@]}"
    return $?
}

# Function to run full scan
run_full_scan() {
    print_status "Running full system scan..."
    check_root
    python3 unsafe_file_scanner.py --verbose /etc /bin /usr/bin /sbin /usr/sbin /var /opt /home
    return $?
}

# Function to run custom scan
run_custom_scan() {
    local dirs=("$@")
    print_status "Running custom scan on: ${dirs[*]}"
    python3 unsafe_file_scanner.py --verbose "${dirs[@]}"
    return $?
}

# Parse command line arguments
CONFIG_FILE=""
OUTPUT_FILE=""
VERBOSE=""
QUICK=false
FULL=false
TEST=false
DIRECTORIES=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -q|--quick)
            QUICK=true
            shift
            ;;
        -f|--full)
            FULL=true
            shift
            ;;
        --test)
            TEST=true
            shift
            ;;
        -*)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
        *)
            DIRECTORIES+=("$1")
            shift
            ;;
    esac
done

# Build command
CMD="python3 unsafe_file_scanner.py"

if [[ -n "$CONFIG_FILE" ]]; then
    CMD="$CMD --config $CONFIG_FILE"
fi

if [[ -n "$OUTPUT_FILE" ]]; then
    CMD="$CMD --output $OUTPUT_FILE"
fi

if [[ -n "$VERBOSE" ]]; then
    CMD="$CMD $VERBOSE"
fi

# Execute based on options
if [[ "$TEST" == true ]]; then
    run_test
elif [[ "$QUICK" == true ]]; then
    run_quick_scan
elif [[ "$FULL" == true ]]; then
    run_full_scan
elif [[ ${#DIRECTORIES[@]} -gt 0 ]]; then
    run_custom_scan "${DIRECTORIES[@]}"
else
    # Default scan
    print_status "Running default scan on common directories..."
    $CMD "${DEFAULT_DIRS[@]}"
    EXIT_CODE=$?
    
    if [[ $EXIT_CODE -eq 0 ]]; then
        print_success "Scan completed - No unsafe files found!"
    elif [[ $EXIT_CODE -eq 1 ]]; then
        print_warning "Scan completed - Unsafe files detected!"
    else
        print_error "Scan failed with exit code: $EXIT_CODE"
    fi
    
    exit $EXIT_CODE
fi
