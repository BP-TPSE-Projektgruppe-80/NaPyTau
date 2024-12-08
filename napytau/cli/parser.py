import argparse
from napytau.cli.cli_arguments import CLIArguments
from napytau.import_export.import_export import IMPORT_FORMATS, IMPORT_FORMAT_NAPATAU


def parse_cli_arguments() -> CLIArguments:
    parser = argparse.ArgumentParser(description="Mockup for NaPyTau")
    parser.add_argument(
        "--headless", action="store_true", help="Run the application without GUI"
    )
    parser.add_argument(
        "--dataset_format",
        type=str,
        default=IMPORT_FORMAT_NAPATAU,
        const=IMPORT_FORMAT_NAPATAU,
        nargs="?",
        choices=IMPORT_FORMATS,
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
