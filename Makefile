# Makefile - Bootstrap ambiente Jupyter reproducible
# Supporta:
# - Ubuntu 24 (Debian-based)
# - Garuda Linux (Arch-based)

PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

.PHONY: help install system check-distro venv deps run freeze clean

help:
	@echo "Targets:"
	@echo "  make install   -> full setup (python + venv + deps)"
	@echo "  make system    -> install python (distro-based)"
	@echo "  make venv      -> create virtualenv"
	@echo "  make deps      -> install dependencies"
	@echo "  make run       -> start jupyter lab"
	@echo "  make freeze    -> update requirements.txt"
	@echo "  make clean     -> remove virtualenv"

# Full setup
install: check-distro system venv deps

# Detect supported distro
check-distro:
	@echo "Checking supported distro..."
	@if [ -f /etc/debian_version ]; then \
		echo "Detected Debian/Ubuntu (OK)"; \
	elif [ -f /etc/arch-release ]; then \
		echo "Detected Arch/Garuda (OK)"; \
	else \
		echo "Unsupported distro. Only Ubuntu 24 and Garuda Linux are supported."; \
		exit 1; \
	fi

# Install Python depending on distro
system:
	@echo "Installing Python..."
	@if [ -f /etc/debian_version ]; then \
		echo "Installing on Ubuntu/Debian..."; \
		sudo apt update; \
		sudo apt install -y python3 python3-venv python3-pip; \
	elif [ -f /etc/arch-release ]; then \
		echo "Installing on Arch/Garuda..."; \
		sudo pacman -Sy --noconfirm python python-pip; \
	fi

# Create virtualenv (only if not exists)
venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtualenv..."; \
		$(PYTHON) -m venv $(VENV); \
	else \
		echo "Virtualenv already exists"; \
	fi

# Install dependencies
deps:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	@if [ -f requirements.txt ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		$(PIP) install jupyterlab pandas requests python-dotenv jupytext; \
	fi

# Freeze dependencies
freeze:
	$(PIP) freeze > requirements.txt

# Run Jupyter Lab
run:
	@echo "Starting Jupyter Lab..."
	$(PY) -m jupyter lab

# Clean environment
clean:
	rm -rf $(VENV)
