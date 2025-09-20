@echo off
REM Unsafe File Scanner - Windows Batch Script
REM This script provides easy execution of the unsafe file scanner on Windows

setlocal enabledelayedexpansion

REM Default directories to scan
set DEFAULT_DIRS=C:\Windows\System32 C:\Program Files C:\Users

REM Parse command line arguments
set CONFIG_FILE=
set OUTPUT_FILE=
set VERBOSE=
set QUICK=false
set FULL=false
set TEST=false
set DIRECTORIES=

:parse_args
if "%~1"=="" goto :execute
if "%~1"=="-h" goto :show_help
if "%~1"=="--help" goto :show_help
if "%~1"=="-c" (
    set CONFIG_FILE=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="--config" (
    set CONFIG_FILE=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="-o" (
    set OUTPUT_FILE=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="--output" (
    set OUTPUT_FILE=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="-v" (
    set VERBOSE=--verbose
    shift
    goto :parse_args
)
if "%~1"=="--verbose" (
    set VERBOSE=--verbose
    shift
    goto :parse_args
)
if "%~1"=="-q" (
    set QUICK=true
    shift
    goto :parse_args
)
if "%~1"=="--quick" (
    set QUICK=true
    shift
    goto :parse_args
)
if "%~1"=="-f" (
    set FULL=true
    shift
    goto :parse_args
)
if "%~1"=="--full" (
    set FULL=true
    shift
    goto :parse_args
)
if "%~1"=="--test" (
    set TEST=true
    shift
    goto :parse_args
)
if "%~1"=="--" goto :execute
set DIRECTORIES=%DIRECTORIES% %~1
shift
goto :parse_args

:show_help
echo Unsafe File Scanner - Windows Batch Script
echo Usage: %0 [OPTIONS] [DIRECTORIES...]
echo.
echo Options:
echo   -h, --help              Show this help message
echo   -c, --config FILE       Use custom configuration file
echo   -o, --output FILE       Save report to file
echo   -v, --verbose           Enable verbose output
echo   -q, --quick             Quick scan (common directories only)
echo   -f, --full              Full system scan (requires admin)
echo   --test                  Run test scan with sample files
echo.
echo Examples:
echo   %0                                    # Scan default directories
echo   %0 -q                                 # Quick scan
echo   %0 -f                                 # Full system scan
echo   %0 C:\Users C:\Program Files          # Scan specific directories
echo   %0 -c config.json -o report.json     # Use custom config and output
echo   %0 --test                             # Run test scan
goto :end

:execute
REM Build command
set CMD=python unsafe_file_scanner.py

if not "%CONFIG_FILE%"=="" (
    set CMD=%CMD% --config %CONFIG_FILE%
)

if not "%OUTPUT_FILE%"=="" (
    set CMD=%CMD% --output %OUTPUT_FILE%
)

if not "%VERBOSE%"=="" (
    set CMD=%CMD% %VERBOSE%
)

REM Execute based on options
if "%TEST%"=="true" (
    echo [INFO] Running test scan with sample files...
    python test_scanner.py
    goto :end
)

if "%QUICK%"=="true" (
    echo [INFO] Running quick scan on common directories...
    %CMD% %DEFAULT_DIRS%
    goto :end
)

if "%FULL%"=="true" (
    echo [INFO] Running full system scan...
    echo [WARNING] Running as administrator. This may scan system-protected files.
    pause
    %CMD% C:\Windows\System32 C:\Program Files C:\Program Files (x86) C:\Users C:\ProgramData
    goto :end
)

if not "%DIRECTORIES%"=="" (
    echo [INFO] Running custom scan on: %DIRECTORIES%
    %CMD% %DIRECTORIES%
    goto :end
)

REM Default scan
echo [INFO] Running default scan on common directories...
%CMD% %DEFAULT_DIRS%

:end
