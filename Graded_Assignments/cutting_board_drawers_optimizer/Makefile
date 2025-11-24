.PHONY: setup-venv install install-dev lint format lint-fix test

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip

setup-venv:
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip setuptools wheel

install: setup-venv
	$(PIP) install -e .

install-dev: setup-venv
	$(PIP) install -e '.[dev]'

lint: setup-venv
	$(PYTHON) -m pylint ./src/

format: setup-venv
	$(PYTHON) -m autopep8 --in-place --aggressive --aggressive **/*.py

lint-fix: format lint

test: setup-venv
	$(PYTHON) -m pytest