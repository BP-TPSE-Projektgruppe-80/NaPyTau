from typing import Optional

from napytau.util.coalesce import coalesce
from argparse import Namespace


class CLIArguments:
    headless: bool
    dataset_format: str
    setup_files_directory: Optional[str]
    fit_file_path: Optional[str]

    def __init__(self, raw_args: Namespace):
        self.headless = coalesce(raw_args.headless, False)
        self.dataset_format = raw_args.dataset_format
        self.setup_files_directory = raw_args.setup_files_directory
        self.fit_file_path = raw_args.fit_file

    def is_headless(self) -> bool:
        return self.headless

    def get_dataset_format(self) -> str:
        return self.dataset_format

    def get_setup_files_directory_path(self) -> Optional[str]:
        return self.setup_files_directory

    def get_fit_file_path(self) -> Optional[str]:
        return self.fit_file_path
