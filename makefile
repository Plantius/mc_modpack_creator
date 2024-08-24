# Variables
PYTHON=python3
PIP=$(PYTHON) -m pip
VENV_DIR=venv
REQUIREMENTS=requirements.txt

# Default target: Set it to help
.DEFAULT_GOAL := help

# Help
help:
	@echo "Available commands:"
	@echo "  make venv          - Create a virtual environment"
	@echo "  make install       - Install dependencies"
	@echo "  make run           - Run the project"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Check code style with flake8"
	@echo "  make clean         - Remove temporary files"
	@echo "  make clean-venv    - Remove virtual environment"

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created."

# Install dependencies
install: venv
	@echo "Installing dependencies..."
	$(VENV_DIR)/bin/$(PIP) install -r $(REQUIREMENTS)
	@echo "Dependencies installed."

# Run the project
run: install
	@echo "Running the project..."
	$(VENV_DIR)/bin/$(PYTHON) -m project

# Run tests (Assumes you have tests set up, modify as needed)
test: install
	@echo "Running tests..."
	$(VENV_DIR)/bin/$(PYTHON) -m unittest discover -s tests

# Lint the code using flake8 (Install flake8 via requirements.txt)
lint: install
	@echo "Checking code style with flake8..."
	$(VENV_DIR)/bin/flake8 .

# Clean temporary files
clean:
	@echo "Cleaning up..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	@echo "Temporary files removed."

# Clean the virtual environment
clean-venv:
	@echo "Removing virtual environment..."
	rm -rf $(VENV_DIR)
	@echo "Virtual environment removed."

.PHONY: help venv install run test lint clean clean-venv
