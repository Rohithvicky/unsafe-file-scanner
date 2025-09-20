# Unsafe File Scanner - Makefile
# This Makefile provides convenient commands for development and testing

.PHONY: help install test clean format lint demo run-example

# Default target
help:
	@echo "Unsafe File Scanner - Available Commands"
	@echo "========================================"
	@echo "install     - Install the package and dependencies"
	@echo "test        - Run the test suite"
	@echo "demo        - Run the demo script"
	@echo "format      - Format code with black"
	@echo "lint        - Run linting checks"
	@echo "clean       - Clean up generated files"
	@echo "run-example - Run example scan"
	@echo "help        - Show this help message"

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -e .

# Run tests
test:
	python -m pytest test_scanner.py -v
	python test_scanner.py

# Run demo
demo:
	python demo.py

# Format code
format:
	black unsafe_file_scanner.py test_scanner.py demo.py
	black --check unsafe_file_scanner.py test_scanner.py demo.py

# Run linting
lint:
	flake8 unsafe_file_scanner.py test_scanner.py demo.py
	mypy unsafe_file_scanner.py

# Clean up generated files
clean:
	rm -f *.log
	rm -f *.json
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

# Run example scan
run-example:
	python unsafe_file_scanner.py --verbose /tmp

# Run quick scan
quick-scan:
	python unsafe_file_scanner.py --verbose /etc /bin /usr/bin

# Run with custom config
custom-scan:
	python unsafe_file_scanner.py --config advanced_config.json --output custom_report.json --verbose /tmp

# Development setup
dev-setup: install
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify installation"
	@echo "Run 'make demo' to see the scanner in action"

# Full test suite
test-full: clean test demo
	@echo "Full test suite completed!"

# Build package
build:
	python setup.py sdist bdist_wheel

# Install package
install-package: build
	pip install dist/*.whl

# Uninstall package
uninstall:
	pip uninstall unsafe-file-scanner -y
