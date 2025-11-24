--setup:
	@python3 -m venv ./.venv
	@. ./.venv/bin/activate

install: --setup
	pip3 install '.'

install-dev: --setup
	pip3 install '.[dev]'

lint: --setup
	pylint ./src/

format:
	autopep8 --in-place --aggressive --aggressive **/*.py

lint-fix: --setup format lint

test: --setup
	pytest
