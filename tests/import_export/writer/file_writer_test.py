import unittest
from pathlib import PurePath
from unittest.mock import MagicMock, patch


class FileReaderUnitTest(unittest.TestCase):
    def test_writesRowsToTheFileAtTheGivenPath(self):
        """Writes rows to the file at the given path."""
        open_mock = MagicMock()

        with patch("builtins.open", open_mock):
            from napytau.import_export.writer.file_writer import FileWriter

            FileWriter.write_rows(PurePath("test.txt"), ["row1", "row2"])
            open_mock.assert_called_once_with(PurePath("test.txt"), "w")
            write_function_mock = open_mock.return_value.__enter__.return_value.write
            self.assertEqual(write_function_mock.call_count, 4)
            self.assertEqual(write_function_mock.call_args_list[0].args[0], "row1")
            self.assertEqual(write_function_mock.call_args_list[1].args[0], "\n")
            self.assertEqual(write_function_mock.call_args_list[2].args[0], "row2")
            self.assertEqual(write_function_mock.call_args_list[3].args[0], "\n")

    def test_writesTextToTheFileAtTheGivenPath(self):
        """Writes text to the file at the given path."""
        open_mock = MagicMock()

        with patch("builtins.open", open_mock):
            from napytau.import_export.writer.file_writer import FileWriter

            FileWriter.write_text(PurePath("test.txt"), "text")
            open_mock.assert_called_once_with(PurePath("test.txt"), "w")
            write_function_mock = open_mock.return_value.__enter__.return_value.write
            write_function_mock.assert_called_once_with("text")


if __name__ == "__main__":
    unittest.main()
