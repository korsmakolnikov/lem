# Makefile - Bootstrap ambiente Jupyter reproducible
# Supporta:
# - Ubuntu 24 (Debian-based)
# - Garuda Linux (Arch-based)

PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
JUPYTEXT := $(VENV)/bin/jupytext

.PHONY: help install system check-distro venv deps run freeze clean

.DEFAULT_GOAL := run

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
install:
	@$(MAKE) check-distro
	@$(MAKE) system
	@$(MAKE) venv
	@$(MAKE) env-file
	@$(MAKE) deps
	@$(MAKE) eol

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
	@echo "Creating virtualenv..."
	@if ! command -v python3 >/dev/null 2>&1; then \
		echo "ERROR: python3 not found"; \
		exit 1; \
	fi

	@python3 -m venv $(VENV) || { \
		echo "ERROR: Failed to create virtualenv. Trying to fix..."; \
		if [ -f /etc/debian_version ]; then \
			echo "Installing python3-venv..."; \
			sudo apt install -y python3-venv; \
		elif [ -f /etc/arch-release ]; then \
			echo "Arch usually has venv included"; \
		fi; \
		echo "Retrying..."; \
		python3 -m venv $(VENV); \
	}

	@if [ ! -d "$(VENV)" ]; then \
		echo "ERROR: venv creation failed"; \
		exit 1; \
	fi

	@echo "Virtualenv created successfully"

# Install dependencies
deps:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	@if [ -f requirements.txt ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		$(PIP) install pyright black ruff jupyterlab pandas requests python-dotenv jupytext matplotlib; \
	fi

# Copy the env file
env-file:
	@if [ ! -f .env ]; then \
		echo "Copying the env placeholder: please fill the fields..."; \ 
	 	cp -n .env.dist .env; \
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

jupytext:
	@echo "Checking Jupytext..."
	@command -v $(JUPYTEXT) >/dev/null 2>&1 || { echo "Jupytext not installed"; exit 1; }
	@echo "Converting .py files in notebooks/..."
	@find notebooks -name "*.py" -exec $(JUPYTEXT) --to notebook {} \;

eol:
	@echo "End of line check..."
