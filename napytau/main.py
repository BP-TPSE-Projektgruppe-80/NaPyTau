# Compilation mode, standalone everywhere, except on macOS there app bundle
# nuitka-project-if: {OS} in ("Windows", "Linux", "FreeBSD"):
#    nuitka-project: --onefile
# nuitka-project-if: {OS} == "Darwin":
#    nuitka-project: --standalone
#    nuitka-project: --macos-create-app-bundle
#
from napytau.gui.app import init as init_gui
from napytau.headless.headless_mockup import init as init_headless
from napytau.cli.parser import parse_cli_arguments


def main() -> None:
    args = parse_cli_arguments()

    if args.headless:
        init_headless(args)
    else:
        init_gui(args)


if __name__ == "__main__":
    main()
