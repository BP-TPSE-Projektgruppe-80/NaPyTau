import unittest
from pathlib import PurePath
from unittest.mock import MagicMock, patch


def set_up_mocks() -> (MagicMock, MagicMock):
    path_mock = MagicMock()
    isfile_mock = MagicMock()
    path_mock.isfile = isfile_mock
    return path_mock, isfile_mock


class FileReaderUnitTest(unittest.TestCase):
    def test_raisesAnErrorIfTheFileDoesNotExistWhenReadingRows(self):
        """Raises an error if the file does not exist when reading rows."""
        path_mock, isfile_mock = set_up_mocks()
        isfile_mock.return_value = False
        with patch.dict("sys.modules", {"os.path": path_mock}):
            from napytau.import_export.reader.file_reader import FileReader

            with self.assertRaises(FileNotFoundError):
                FileReader.read_rows(PurePath("test.txt"))

    def test_returnsTheRowsOfTheFile(self):
        """Returns the rows of the file."""
        path_mock, isfile_mock = set_up_mocks()
        isfile_mock.return_value = True
        with patch.dict("sys.modules", {"os.path": path_mock}):
            from napytau.import_export.reader.file_reader import FileReader

            with patch("builtins.open", MagicMock()) as open_mock:
                open_mock.return_value.__enter__.return_value.readlines.return_value = [
                    "row1",
                    "row2",
                ]
                rows = FileReader.read_rows(PurePath("test.txt"))
                self.assertEqual(rows, ["row1", "row2"])

    def test_raisesAnErrorIfTheFileDoesNotExistWhenReadingText(self):
        """Raises an error if the file does not exist when reading text."""
        path_mock, isfile_mock = set_up_mocks()
        isfile_mock.return_value = False
        with patch.dict("sys.modules", {"os.path": path_mock}):
            from napytau.import_export.reader.file_reader import FileReader

            with self.assertRaises(FileNotFoundError):
                FileReader.read_text(PurePath("test.txt"))

    def test_returnsTheTextOfTheFile(self):
        """Returns the text of the file."""
        path_mock, isfile_mock = set_up_mocks()
        isfile_mock.return_value = True
        with patch.dict("sys.modules", {"os.path": path_mock}):
            from napytau.import_export.reader.file_reader import FileReader

            with patch("builtins.open", MagicMock()) as open_mock:
                open_mock.return_value.__enter__.return_value.read.return_value = "text"
                text = FileReader.read_text(PurePath("test.txt"))
                self.assertEqual(text, "text")


if __name__ == "__main__":
    unittest.main()
