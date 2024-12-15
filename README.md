#  <center> <img src="./metadata/napytau_logo.jpg" width="50" />  &nbsp; &nbsp; NaPyTau &nbsp; &nbsp; <img src="./metadata/napytau_logo.jpg" width="50" />  </center> 

----
[![CI Action Status](https://github.com/BP-TPSE-Projektgruppe-80/NaPyTau/workflows/ci/badge.svg)](https://github.com/BP-TPSE-Projektgruppe-80/NaPyTau/actions)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

<!-- TODO: add introduction section, explaining the software and showing its functionality -->

## Installation

### Distributions

With every release, we provide pre-built binaries for Windows, and Linux. You can find the latest releases under [releases](https://github.com/BP-TPSE-Projektgruppe-80/NaPyTau/releases)
Note that we do not provide pre-built binaries for MacOS, however, you can build the project from source.

### Building from source

To build the project from source requires the following dependencies:

- [Python 3.12 or greater](https://www.python.org/downloads/)
- [PIP](https://pypi.org/project/pip/#description)
- [UV](https://docs.astral.sh/uv/getting-started/installation/)
- One of the following C compilers:
  - GCC (MinGW on Windows)
  - Clang
  - MSVC

To build the project from source, follow these steps:

1. Clone the repository
2. Run in the projects root directory:
    ```bash
    $ uv pip compile pyproject.toml > requirements.txt && uv pip install --system -r requirements.txt
    $ python -m nuitka  --mode=app --assume-yes-for-downloads --output-dir=build --script-name=napytau/main.py --enable-plugins=tk-inter
    ```
Notes
 - We install the dependencies via pip rather than uv because nuitka has so far not been able to handle the dependencies installed via uv.
 - Optionally you can specify the C-compiler to use with for example `--mingw64` for MinGW on Windows.
 - To include the provided icon in the executable, add `--windows-icon-from-ico=metadata/napytau_logo.ico` or `--linux-icon=metadata/napytau_logo.jpg` to the build command.
   
## Contributing

While the project is open source, we do not accept contributions from the public.
This is due to the project being part of a university course and the code being graded.
However, you are free to file issues and suggest features. Once the course is completed
the project will be transferred to the commissioning party who will decide on the future of the project.

## Development

To get started with development, follow these steps:

1. Clone the repository
2. Create a virtual environment with `uv venv --python=$PythonVersion` where `$PythonVersion` is greater than 3.12. Note that there is a bug in Python 3.13 that leads to the core dependency TCL not being installed correctly on Windows.
3. Run `uv sync --dev`

Some useful commands during development are:

- `uvx tomlscript run` to run the project
- `uvx tomlscript test` to run the tests
- `uvx tomlscript lint` to lint the code
- `uvx tomlscript format` to format the code

Please note that the project is focused on modularity and readability. We use type hints and docstrings to ensure that the code is self-explanatory.
Before submitting a pull request, make sure that the code is formatted and that the tests pass.
