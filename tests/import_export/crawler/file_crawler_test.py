import unittest
from pathlib import PurePath
from re import compile
from unittest.mock import MagicMock, patch


def set_up_mocks() -> (
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
):
    os_module_mock = MagicMock()
    re_module_mock = MagicMock()
    walk_mock = MagicMock()
    path_mock = MagicMock()
    isdir_mock = MagicMock()
    regex_match_mock = MagicMock()
    os_module_mock.walk = walk_mock
    os_module_mock.path = path_mock
    os_module_mock.path.isdir = isdir_mock
    re_module_mock.match = regex_match_mock

    return (
        os_module_mock,
        re_module_mock,
        walk_mock,
        path_mock,
        isdir_mock,
        regex_match_mock,
    )


class FileCrawlerUnitTest(unittest.TestCase):
    def test_raisesErrorIfProvidedPathIsNotADirectory(self):
        """Raises an error if the provided path is not a directory"""
        os_module_mock, re_module_mock, _, path_mock, isdir_mock, _ = set_up_mocks()
        isdir_mock.return_value = False
        with patch.dict(
            "sys.modules",
            {
                "os": os_module_mock,
                "re": re_module_mock,
                "os.path": path_mock,
            },
        ):
            from napytau.import_export.crawler.file_crawler import FileCrawler

            file_crawler = FileCrawler([], lambda x: x)
            with self.assertRaises(ValueError):
                file_crawler.crawl(PurePath("not_a_directory"))

    def test_returnsEmptyArrayIfProvidedDirectoryEmpty(self):
        """Returns an empty array if the provided directory is empty"""
        os_module_mock, re_module_mock, walk_mock, path_mock, isdir_mock, _ = (
            set_up_mocks()
        )
        isdir_mock.return_value = True
        walk_mock.return_value = []
        with patch.dict(
            "sys.modules",
            {
                "os": os_module_mock,
                "re": re_module_mock,
                "os.path": path_mock,
            },
        ):
            from napytau.import_export.crawler.file_crawler import FileCrawler

            file_crawler = FileCrawler([], lambda x: x)
            self.assertEqual(file_crawler.crawl(PurePath("some/directory")), [])

    def test_doesNotAddFilesIfNoFilesMatchThePattern(self):
        """Does not add files if no files match the pattern"""
        (
            os_module_mock,
            re_module_mock,
            walk_mock,
            path_mock,
            isdir_mock,
            regex_match_mock,
        ) = set_up_mocks()
        isdir_mock.return_value = True
        walk_mock.return_value = [("root", [], ["file1", "file2"])]
        regex_match_mock.return_value = False
        with patch.dict(
            "sys.modules",
            {
                "os": os_module_mock,
                "re": re_module_mock,
                "os.path": path_mock,
            },
        ):
            from napytau.import_export.crawler.file_crawler import FileCrawler

            file_crawler = FileCrawler(
                [compile("pattern1"), compile("pattern2")], lambda x: x
            )
            self.assertEqual(file_crawler.crawl(PurePath("some/directory")), [])

    def test_addsFilesIfFilesMatchThePatternAndMapsThemWithTheProvidedFactory(self):
        """Adds files if files match the pattern and maps them with the provided factory"""  # noqa: E501
        (
            os_module_mock,
            re_module_mock,
            walk_mock,
            path_mock,
            isdir_mock,
            regex_match_mock,
        ) = set_up_mocks()
        isdir_mock.return_value = True
        walk_mock.return_value = [("root", [], ["file1", "file2"])]
        regex_match_mock.side_effect = lambda pattern, file: file == "file2"
        with patch.dict(
            "sys.modules",
            {
                "os": os_module_mock,
                "re": re_module_mock,
                "os.path": path_mock,
            },
        ):
            from napytau.import_export.crawler.file_crawler import FileCrawler

            factory_mock = MagicMock()
            factory_mock.return_value = ["root/file2"]

            file_crawler = FileCrawler(
                [compile("pattern1"), compile("pattern2")], factory_mock
            )
            self.assertEqual(
                file_crawler.crawl(PurePath("some/directory")), [["root/file2"]]
            )
            self.assertEqual(
                factory_mock.mock_calls[0].args, ([PurePath("root/file2")],)
            )


if __name__ == "__main__":
    unittest.main()
