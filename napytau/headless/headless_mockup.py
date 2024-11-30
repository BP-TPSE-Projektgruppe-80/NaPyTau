from napytau.cli.cli_arguments import CLIArguments
from napytau.ingest.ingest_mockup import ingest_file


def init(cli_arguments: CLIArguments) -> None:
    print("running headless mockup")
    if cli_arguments.has_filename():
        print(
            f"{cli_arguments.get_filename()}:\n{ingest_file(cli_arguments.get_filename())}"
        )
