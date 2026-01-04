.PHONY: help test test-verbose test-basic test-inheritance test-decorators coverage clean install-dev examples

help:
	@echo "Available commands:"
	@echo "  make test              - Run all tests"
	@echo "  make test-verbose      - Run tests with verbose output"
	@echo "  make test-basic        - Run basic class analysis tests only"
	@echo "  make test-inheritance  - Run inheritance analysis tests only"
	@echo "  make test-decorators   - Run decorator analysis tests only"
	@echo "  make coverage          - Run tests with coverage report"
	@echo "  make examples          - Run all example scripts"
	@echo "  make install-dev       - Install development dependencies"
	@echo "  make clean             - Clean up test artifacts"

test:
	python3 -m pytest tests/

test-verbose:
	python3 -m pytest tests/ -v

test-basic:
	python3 -m pytest tests/ -m basic -v

test-inheritance:
	python3 -m pytest tests/ -m inheritance -v

test-decorators:
	python3 -m pytest tests/ -m decorators -v

coverage:
	python3 -m pytest tests/ --cov=scripts --cov=examples --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

examples:
	@echo "Running example 01..."
	python3 examples/01_basic_class_analysis.py
	@echo "\nRunning example 02..."
	python3 examples/02_inheritance_analysis.py
	@echo "\nRunning example 03..."
	python3 examples/03_decorator_analysis.py

install-dev:
	pip install -r requirements-dev.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -f /tmp/analyze_sample_*.py

