## Setup

Make sure you have the following installed:

- Python 3.10 or later
- Pip
- uv
- (optional) npm

## Development

1. Clone the repository
2. Create a virtual environment with `uv venv --python=$PythonVersion` where `$PythonVersion` is greater than 3.10.
3. Run `uv sync --extra dev`

To run the project use `uvx tomlscript run`, optionally you can use nodemon for hot reloading with the command `nodemon --exec uvx tomlscript run`.

To run test use `uvx tomlscript test`.
