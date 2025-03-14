from napytau.gui.app import init as init_gui
from napytau.headless.headless_kernel import init as init_headless
from napytau.cli.parser import parse_cli_arguments


def main() -> None:
    args = parse_cli_arguments()

    if args.headless:
        init_headless(args)
    else:
        init_gui(args)


if __name__ == "__main__":
    main()
