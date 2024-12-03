import argparse
from napytau.cli.cli_arguments import CLIArguments
from napytau.ingest.ingest import INGEST_FORMATS


def parse_cli_arguments() -> CLIArguments:
    parser = argparse.ArgumentParser(description="Mockup for NaPyTau")
    parser.add_argument(
        "--headless", action="store_true", help="Run the application without GUI"
    )
    parser.add_argument(
        "--dataset_format",
        type=str,
        default="napatau",
        const="napatau",
        nargs="?",
        choices=INGEST_FORMATS,
        help="Format of the dataset to ingest",
    )
    parser.add_argument(
        "--setup_files_directory",
        type=str,
        help="Path to the directory containing either setup files or subdirectories "
        "with setup files",
    )
    parser.add_argument(
        "--fit_file",
        type=str,
        help="Path to a fit file to use instead of the one found in the setup files",
    )

    return CLIArguments(parser.parse_args())
