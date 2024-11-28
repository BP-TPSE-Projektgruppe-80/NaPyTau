from napytau.util.coalesce import coalesce
from argparse import Namespace


class CLIArguments:
    headless: bool
    filename: str

    def __init__(self, raw_args: Namespace):
        self.headless = coalesce(raw_args.headless, False)
        self.filename = raw_args.filename

    def __str__(self) -> str:
        return f"CLIArguments(headless={self.headless}, filename={self.filename})"

    def is_headless(self) -> bool:
        return self.headless

    def has_filename(self) -> bool:
        return self.filename is not None

    def get_filename(self) -> str:
        return self.filename
