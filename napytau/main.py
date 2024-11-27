from gui.ui_mockup import init as init_gui
from headless.headless_mockup import init as init_headless
from cli.parser import parse_cli_arguments


def main():
    args = parse_cli_arguments()

    if args.headless:
        init_headless(args)
    else:
        init_gui(args)


if __name__ == "__main__":
    main()
