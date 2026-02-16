# Cutting Board Drawers Optimizer

[![CI](https://github.com/SayHeyD/teko-turtle/actions/workflows/cutting-board-drawers-optimizer.yml/badge.svg)](https://github.com/SayHeyD/teko-turtle/actions/workflows/cutting-board-drawers-optimizer.yml)

-----

## Table of Contents

- [Prerequisites](#prerequisites)   
- [Installation](#installation)
- [License](#license)

## Prerequisites

[Hatch 1.16](https://hatch.pypa.io/1.16/) or newer is required to use all development commands.

## Installation

```shell
pip install cutting-board-drawers-optimizer
```

### Run tests

```shell
hatch test
```

### Linting

Fix issues automatically:

```shell
hatch fmt
```

Check only:

```shell
hatch fmt --check
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
