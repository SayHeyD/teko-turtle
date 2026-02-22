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

## Usage

First of all, add some drawers and cutting boards.

![Create Cutting Boards](./docs/create_cutting_board.png)

![Create Drawers](./docs/create_drawer.png)

After adding some drawers and cutting boards, they show up on the table.

![Cutting Board Table](./docs/cutting_board_table.png)

![Drawer Table](./docs/drawer_table.png)

Then you can input your budget and total number of boards.

![Input Budget and Boards](./docs/optimize_settings.png)

After confirming, you will be shown the results.

![Results](./docs/results.png)
