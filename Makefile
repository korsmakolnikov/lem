# =============================================================================
# Makefile
# supported distros: Arch Linux, Ubuntu 24
# =============================================================================

VENV_DIR  := .venv
JUPYTEXT  := $(VENV_DIR)/bin/jupytext
JUPYTER   := $(VENV_DIR)/bin/jupyter

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
	@echo "    make install-system   Install system Python + uv"
	@echo "    make venv             Create the virtual environment in $(VENV_DIR)/"
	@echo "    make install          Install project dependencies in the venv"
	@echo "    make install-dev      Install development dependencies (pyright, black, ruff)"
	@echo "    make run              Run jupyter notebook server"
	@echo "    make clean            Remove venv and output"
	@echo "    make activate         Activate the virtual environment"
	@echo "    make all              venv + install + run"
	@echo ""

# -----------------------------------------------------------------------------
# install-system  →  system dependencies (Python, uv)
# Arch:   pacman
# Ubuntu: apt
# -----------------------------------------------------------------------------
.PHONY: install-system
install-system:
ifeq ($(DISTRO),arch)
	@echo "[arch] Installing python + uv..."
	sudo pacman -Sy --noconfirm python uv
else ifeq ($(DISTRO),ubuntu)
	@echo "[ubuntu] Installing python3 + uv..."
	sudo apt-get update -qq
	sudo apt-get install -y python3 python3-dev build-essential
	curl -LsSf https://astral.sh/uv/install.sh | sh
else
	@echo "[warn] Distro unknown ($(DISTRO))."
	@echo "       please install manually: python3, uv"
endif

# -----------------------------------------------------------------------------
# venv  →  create the virtual environment
# -----------------------------------------------------------------------------
.PHONY: venv
venv:
	@echo "[venv] Creating virtual environment in $(VENV_DIR)/ ..."
	uv venv $(VENV_DIR)
	@echo "[venv] Virtual environment ready ✓"
	@echo "       activate with:  source $(VENV_DIR)/bin/activate"

# -----------------------------------------------------------------------------
# install  →  project dependencies
# -----------------------------------------------------------------------------
.PHONY: install
install: $(VENV_DIR)/bin/activate
	@echo "[uv] Installing deps..."
	uv sync
	@echo "[uv] deps installed ✓"

# -----------------------------------------------------------------------------
# install-dev  →  development dependencies (pyright, black, ruff)
# -----------------------------------------------------------------------------
.PHONY: install-dev
install-dev: $(VENV_DIR)/bin/activate
	@echo "[uv] Installing dev deps..."
	uv sync --dev
	@echo "[uv] dev deps installed ✓"
	$(JUPYTER) labextension enable widgetsnbextension

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
	@echo "Starting Jupyter Lab..."
	uv run jupyter lab

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
.PHONY: test
test:
	@echo "Running tests..."
	uv run pytest

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
