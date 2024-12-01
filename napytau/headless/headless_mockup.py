from napytau.cli.cli_arguments import CLIArguments
from napytau.ingest.ingest import ingest_napatau_format_from_files


def init(cli_arguments: CLIArguments) -> None:
    print("running headless mockup")
    if cli_arguments.has_filename():
        print(
            f"{cli_arguments.get_filename()}:\n{ingest_napatau_format_from_files(cli_arguments.get_filename())}"
        )
