# Cutting Board Drawer Optimizer

## Setup

1. Create virtual environment
    ```shell
    python3 -m venv ./.venv
    ```
2. Activate venv
    ```shell
    source ./.venv/bin/activate
    ```
3. Install dependencies for development
    ```shell
    pip3 install .[dev]
    ```
   
## Commands

* Lint
    ```shell
    pylint .
    ```
* Fix codestyle (does not fix all linting errors automatically)
    ```shell
    autopep8 --in-place --aggressive --aggressive **/*.py
    ```