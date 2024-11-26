import argparse
from napytau.cli.cli_arguments import CLIArguments


def parse_cli_arguments() -> CLIArguments:
    parser = argparse.ArgumentParser(description="Mockup for NaPyTau")
    parser.add_argument(
        "--headless", action="store_true", help="Run the application without GUI"
    )
    parser.add_argument(
        "--filename",
        type=str,
        help="File to ingest (only for mockup, not used in real application)",
    )

    return CLIArguments(parser.parse_args())
