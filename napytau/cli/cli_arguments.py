from os import getcwd
from typing import Optional

from napytau.util.coalesce import coalesce
from argparse import Namespace


class CLIArguments:
    headless: bool
    dataset_format: str
    data_files_directory: str
    fit_file_path: Optional[str]
    setup_identifier: Optional[str]
    t_hyp_estimate: Optional[float]

    def __init__(self, raw_args: Namespace):
        self.headless = coalesce(raw_args.headless, False)
        self.dataset_format = raw_args.dataset_format
        self.data_files_directory = coalesce(raw_args.data_files_directory, getcwd())
        self.fit_file_path = raw_args.fit_file
        self.setup_identifier = raw_args.setup_identifier
        self.t_hyp_estimate = raw_args.t_hyp_estimate

    def is_headless(self) -> bool:
        return self.headless

    def get_dataset_format(self) -> str:
        return self.dataset_format

    def get_data_files_directory_path(self) -> str:
        return self.data_files_directory

    def get_fit_file_path(self) -> Optional[str]:
        return self.fit_file_path

    def get_setup_identifier(self) -> Optional[str]:
        return self.setup_identifier

    def get_t_hyp_estimate(self) -> Optional[float]:
        return self.t_hyp_estimate
