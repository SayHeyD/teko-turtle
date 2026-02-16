# Cutting Board Drawers Optimizer

[![PyPI - Version](https://img.shields.io/pypi/v/cutting-board-drawers-optimizer.svg)](https://pypi.org/project/cutting-board-drawers-optimizer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cutting-board-drawers-optimizer.svg)](https://pypi.org/project/cutting-board-drawers-optimizer)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```shell
pip install cutting-board-drawers-optimizer
```

### Run tests

```shell
hatch test
```

### Linting

```shell
hatch fmt
```

Fix linting issues:

```shell
hatch fmt --fix
```

### Type checking

```shell
hatch run types:check
```

## Run the application

```shell
hatch run start
```

## Cleanup envs

Can be necessary after e.g. homebrew upgrades of python versions:

```shell
hatch env remove test
```

## License

`cutting-board-drawers-optimizer` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
