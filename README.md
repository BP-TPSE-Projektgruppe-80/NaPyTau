# NaPyTau

----
[![CI Action Status](https://github.com/BP-TPSE-Projektgruppe-80/NaPyTau/workflows/ci/badge.svg)](https://github.com/BP-TPSE-Projektgruppe-80/NaPyTau/actions)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Setup

Make sure you have the following installed:

- Python 3.10 or later
- Pip
- uv
- (optional) npm

## Development

1. Clone the repository
2. Create a virtual environment with `uv venv --python=$PythonVersion` where `$PythonVersion` is greater than 3.10.
3. Run `uv sync`

To run the project use `uvx tomlscript run`, optionally you can use nodemon for hot reloading with the command `nodemon --exec uvx tomlscript run`.

To run test use `uvx tomlscript test`.

To run the linter use `uvx tomlscript lint` or `uvx tomlscript lint-fix` to fix the issues.

