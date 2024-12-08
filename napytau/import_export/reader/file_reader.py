from os.path import isfile
from typing import List

from napytau.import_export.reader.reader import Reader


class FileReader(Reader[str]):
    @staticmethod
    def read_rows(file_path: str) -> List[str]:
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
