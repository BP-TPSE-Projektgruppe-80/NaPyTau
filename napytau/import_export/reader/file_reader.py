from os.path import isfile
from pathlib import PurePath
from typing import List


class FileReader:
    @staticmethod
    def read_rows(file_path: PurePath) -> List[str]:
        if not isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path) as file:
            rows = file.readlines()

        return list(
            map(
                lambda row: str(row),
                rows,
            )
        )

    @staticmethod
    def read_text(file_path: PurePath) -> str:
        if not isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path) as file:
            text = file.read()

        return text
