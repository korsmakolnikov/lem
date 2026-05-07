# =============================================================================
# Makefile
# supported distros: Arch Linux, Ubuntu 24
# =============================================================================

VENV_DIR  := .venv
PYTHON    := python3
PIP       := $(VENV_DIR)/bin/pip
VENV_PY   := $(VENV_DIR)/bin/python
REQ_FILE      := requirements.txt
DEV_REQ_FILE  := requirements-dev.txt
JUPYTEXT := $(VENV_DIR)/bin/jupytext
JUPYTER_LABEXTENTION := $(VENV_DIR)/bin/jupyter

# detect the distro
DISTRO := $(shell \
	if [ -f /etc/arch-release ]; then echo arch; \
	elif grep -qi ubuntu /etc/os-release 2>/dev/null; then echo ubuntu; \
	else echo unknown; fi)

.DEFAULT_GOAL := help

# -----------------------------------------------------------------------------
# help
# -----------------------------------------------------------------------------
.PHONY: help
help:
	@echo ""
	@echo "  Distro: $(DISTRO)"
	@echo ""
	@echo "  Targets available:"
	@echo "    make install-system   Install system Python + pip"
	@echo "    make venv             Create the virtual environment in $(VENV_DIR)/"
	@echo "    make install          Install project dependencies in the venv"
	@echo "    make install-dev      Install develpment dependencies (pyright, black, ruff)"
	@echo "    make run              Run jupyter notebook server"
	@echo "    make clean            Remove venv e output"
	@echo "    make activate         Activate the virtual environment"
	@echo "    make all              venv + install + run"
	@echo ""

# -----------------------------------------------------------------------------
# install-system  →  system dependencies (Python, pip, venv)
# Arch:   pacman
# Ubuntu: apt
# -----------------------------------------------------------------------------
.PHONY: install-system
install-system:
ifeq ($(DISTRO),arch)
	@echo "[arch] Installing python + python-pip + python-virtualenv..."
	sudo pacman -Sy --noconfirm python python-pip python-virtualenv
else ifeq ($(DISTRO),ubuntu)
	@echo "[ubuntu] Installing python3 + pip + venv..."
	sudo apt-get update -qq
	sudo apt-get install -y python3 python3-pip python3-venv python3-dev build-essential
else
	@echo "[warn] Distro unknown ($(DISTRO))."
	@echo "       please install manually: python3, pip, venv"
endif

# -----------------------------------------------------------------------------
# venv  →  create the virtual environment
# -----------------------------------------------------------------------------
.PHONY: venv
venv:
	@echo "[venv] Creating virtual environment in $(VENV_DIR)/ ..."
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip --quiet
	@echo "[venv] Virtual environment ready ✓"
	@echo "       activated with:  source $(VENV_DIR)/bin/activate"

# -----------------------------------------------------------------------------
# install  →  project dependencies (dal requirements.txt)
# -----------------------------------------------------------------------------
.PHONY: install
install: $(VENV_DIR)/bin/activate
	@echo "[pip] installing deps $(REQ_FILE)..."
	$(PIP) install -r $(REQ_FILE)
	$(PIP) install -e .
	@echo "[pip] deps installed ✓"

# -----------------------------------------------------------------------------
# install-dev  →  develpment dependencies (pyright, black, ruff)
# -----------------------------------------------------------------------------
.PHONY: install-dev
install-dev: $(VENV_DIR)/bin/activate
	@echo "[pip] installing dev deps $(DEV_REQ_FILE)..."
	$(PIP) install -r $(DEV_REQ_FILE)
	@echo "[pip] dev deps installed ✓"
	$(JUPYTER_LABEXTENTION) labextension enable widgetsnbextension

$(VENV_DIR)/bin/activate:
	@echo "[err] Virtual environment not found. please run: make venv"
	@exit 1

# -----------------------------------------------------------------------------
# jupytext -> export py notebooks to jupyter notebooks format
# -----------------------------------------------------------------------------
.PHONY: jupytext
jupytext:
	@echo "Checking Jupytext..."
	@command -v $(JUPYTEXT) >/dev/null 2>&1 || { echo "Jupytext not installed"; exit 1; }
	@echo "Converting .py files in notebooks/..."
	@find notebooks -name "*.py" -exec $(JUPYTEXT) --to notebook {} \;

# -----------------------------------------------------------------------------
# run  →  execute jupyter notebook server
# -----------------------------------------------------------------------------
.PHONY: run
run: jupytext
	# $(VENV_PY) main.py
	@echo "Starting Jupyter Lab..."
	$(VENV_PY) -m jupyter lab


# ------------------------------------------------------------------------------
# activate -> activate the virtual environment
# ------------------------------------------------------------------------------
.PHONY: activate
activate:
	source $(VENV_DIR)/bin/activate 


# ------------------------------------------------------------------------------
# env-file -> initialize the .env file
# ------------------------------------------------------------------------------
.PHONY: env-file
env-file:
	@if [ ! -f .env ]; then \
		echo "Copying the env placeholder: please fill the fields..."; \
	 	cp -n .env.dist .env; \
	fi

# -----------------------------------------------------------------------------
# all  →  complete provisioning
# -----------------------------------------------------------------------------
.PHONY: all
all: venv install install-dev run

# -----------------------------------------------------------------------------
# clean
# -----------------------------------------------------------------------------
.PHONY: clean
clean:
	@echo "[clean] removing $(VENV_DIR)/ and output/..."
	rm -rf $(VENV_DIR)
	@echo "[clean] done ✓"
