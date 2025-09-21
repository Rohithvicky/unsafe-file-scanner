# Makefile for Unsafe File Scanner
# Professional development and deployment automation

.PHONY: help install install-dev test lint format clean build docker run-docker docs

# Default target
help:
	@echo "🔒 Unsafe File Scanner - Development Commands"
	@echo "=============================================="
	@echo ""
	@echo "Installation:"
	@echo "  install      Install package in development mode"
	@echo "  install-dev  Install with development dependencies"
	@echo "  install-prod Install production dependencies only"
	@echo ""
	@echo "Development:"
	@echo "  test         Run all tests"
	@echo "  test-cov     Run tests with coverage"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code with black and isort"
	@echo "  type-check   Run type checking with mypy"
	@echo "  security     Run security checks"
	@echo ""
	@echo "Building:"
	@echo "  build        Build package"
	@echo "  clean        Clean build artifacts"
	@echo "  dist         Create distribution packages"
	@echo ""
	@echo "Docker:"
	@echo "  docker       Build Docker image"
	@echo "  run-docker   Run Docker container"
	@echo "  docker-test  Run tests in Docker"
	@echo ""
	@echo "Documentation:"
	@echo "  docs         Build documentation"
	@echo "  docs-serve   Serve documentation locally"
	@echo ""
	@echo "Utilities:"
	@echo "  check        Run all checks (lint, type, test)"
	@echo "  pre-commit   Install pre-commit hooks"
	@echo "  update-deps  Update dependencies"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e .
	pip install -r requirements-dev.txt

install-prod:
	pip install -r requirements.txt
	pip install -e .

# Testing targets
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=unsafe_file_scanner --cov-report=html --cov-report=term

test-fast:
	pytest tests/ -v --tb=short

# Code quality targets
lint:
	flake8 unsafe_file_scanner/ tests/
	black --check unsafe_file_scanner/ tests/
	isort --check-only unsafe_file_scanner/ tests/

format:
	black unsafe_file_scanner/ tests/
	isort unsafe_file_scanner/ tests/

type-check:
	mypy unsafe_file_scanner/ --ignore-missing-imports

security:
	bandit -r unsafe_file_scanner/
	safety check

# Building targets
build:
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

dist: clean build
	@echo "Distribution packages created in dist/"

# Docker targets
docker:
	docker build -t unsafe-file-scanner:latest .

run-docker:
	docker run --rm -it unsafe-file-scanner:latest

docker-test:
	docker build -t unsafe-file-scanner:test .
	docker run --rm unsafe-file-scanner:test pytest tests/

# Documentation targets
docs:
	sphinx-build -b html docs/ docs/_build/html

docs-serve:
	cd docs/_build/html && python -m http.server 8000

# Utility targets
check: lint type-check test
	@echo "✅ All checks passed!"

pre-commit:
	pip install pre-commit
	pre-commit install

update-deps:
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt
	pip install --upgrade -r requirements-dev.txt

# Development workflow
dev-setup: install-dev pre-commit
	@echo "🚀 Development environment ready!"

# CI/CD simulation
ci: lint type-check security test
	@echo "✅ CI pipeline passed!"

# Release preparation
release-check: clean lint type-check security test build
	@echo "✅ Ready for release!"

# Platform-specific installation
install-linux:
	chmod +x install.sh
	./install.sh

install-windows:
	install.bat

install-macos:
	chmod +x install.sh
	./install.sh

# Quick commands
run-cli:
	python -m unsafe_file_scanner.unsafe_file_scanner --help

run-gui:
	python -m unsafe_file_scanner.unsafe_file_scanner_gui

# Performance testing
perf-test:
	pytest tests/ -v --benchmark-only

# Memory profiling
mem-test:
	pytest tests/ -v --memray

# Coverage reporting
coverage-report:
	pytest tests/ --cov=unsafe_file_scanner --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"
