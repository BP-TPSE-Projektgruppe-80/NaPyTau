import unittest
from unittest.mock import MagicMock, patch


def set_up_mocks() -> (MagicMock, MagicMock):
    path_mock = MagicMock()
    isfile_mock = MagicMock()
    path_mock.isfile = isfile_mock
    return path_mock, isfile_mock


class FileReaderUnitTest(unittest.TestCase):
    def test_raisesAnErrorIfTheFileDoesNotExist(self):
        """Raises an error if the file does not exist."""
        path_mock, isfile_mock = set_up_mocks()
        isfile_mock.return_value = False
        with patch.dict("sys.modules", {"os.path": path_mock}):
            from napytau.ingest.reader.file_reader import FileReader

            with self.assertRaises(FileNotFoundError):
                FileReader.read_rows("test.txt")

    def test_returnsTheRowsOfTheFile(self):
        """Returns the rows of the file."""
        path_mock, isfile_mock = set_up_mocks()
        isfile_mock.return_value = True
        with patch.dict("sys.modules", {"os.path": path_mock}):
            from napytau.ingest.reader.file_reader import FileReader

            with patch("builtins.open", MagicMock()) as open_mock:
                open_mock.return_value.__enter__.return_value.readlines.return_value = [
                    "row1",
                    "row2",
                ]
                rows = FileReader.read_rows("test.txt")
                self.assertEqual(rows, ["row1", "row2"])


if __name__ == "__main__":
    unittest.main()
