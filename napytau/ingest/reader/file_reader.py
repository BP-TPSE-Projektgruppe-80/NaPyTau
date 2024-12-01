from typing import List

from napytau.ingest.reader.reader import Reader


class FileReader(Reader[str]):
    @staticmethod
    def read_rows(file_path: str) -> List[str]:
        with open(file_path) as file:
            rows = file.readlines()

        return list(
            map(
                lambda row: str(row),
                rows,
            )
        )
