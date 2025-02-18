from pathlib import PurePath

from napytau.import_export.writer.writer import Writer


class FileWriter(Writer[PurePath]):
    @staticmethod
    def write_rows(file_path: PurePath, rows: list[str]) -> None:
        with open(file_path, "w") as file:
            for row in rows:
                file.write(row)
                file.write("\n")

    @staticmethod
    def write_text(file_path: PurePath, text: str) -> None:
        with open(file_path, "w") as file:
            file.write(text)
