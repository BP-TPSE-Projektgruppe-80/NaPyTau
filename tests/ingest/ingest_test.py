import unittest
from unittest.mock import MagicMock, patch

from napytau.import_export.crawler.napatau_setup_files import NapatauSetupFiles


def set_up_mocks() -> (
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
    MagicMock,
):
    napatau_dataset_factory_module_mock = MagicMock()
    napatau_dataset_factory_mock = MagicMock()
    napatau_dataset_factory_module_mock.NapatauSetupFiles = napatau_dataset_factory_mock
    file_crawler_module_mock = MagicMock()
    file_crawler_mock = MagicMock()
    file_crawler_mock.crawl = MagicMock()
    file_crawler_module_mock.FileCrawler = file_crawler_mock
    file_crawler_module_mock.FileCrawler.return_value = (
        file_crawler_module_mock.FileCrawler
    )
    file_reader_module_mock = MagicMock()
    file_reader_mock = MagicMock()
    file_reader_module_mock.FileReader = file_reader_mock
    read_rows_mock = MagicMock()
    file_reader_mock.read_rows = read_rows_mock
    return (
        napatau_dataset_factory_module_mock,
        file_crawler_module_mock,
        file_reader_module_mock,
    )


class IngestUnitTest(unittest.TestCase):
    def test_instantiatesTheFileCrawlerWithAFitPatternIfNoFitFileIsProvided(self):
        """Instantiates the file crawler with a fit pattern if no fit file is provided."""  # noqa E501
        (
            napatau_dataset_factory_module_mock,
            file_crawler_module_mock,
            file_reader_module_mock,
        ) = set_up_mocks()
        with patch.dict(
            "sys.modules",
            {
                "napytau.import_export.dataset_factory.napatau_dataset_factory": napatau_dataset_factory_module_mock,  # noqa E501
                "napytau.import_export.crawler.file_crawler": file_crawler_module_mock,  # noqa E501
                "napytau.import_export.reader.file_reader": file_reader_module_mock,  # noqa E501
            },
        ):
            from napytau.import_export.import_export import ingest_napatau_format_from_files

            ingest_napatau_format_from_files("test_directory")
            self.assertEqual(
                file_crawler_module_mock.FileCrawler.mock_calls[0].args[0],
                ["v_c", "distances.dat", "norm.fac", ".*.fit"],
            )

    def test_instantiatesTheFileCrawlerWithoutAFitPatternIfAFitFileIsProvided(self):
        """Instantiates the file crawler without a fit pattern if a fit file is provided."""  # noqa E501
        (
            napatau_dataset_factory_module_mock,
            file_crawler_module_mock,
            file_reader_module_mock,
        ) = set_up_mocks()
        with patch.dict(
            "sys.modules",
            {
                "napytau.import_export.dataset_factory.napatau_dataset_factory": napatau_dataset_factory_module_mock,  # noqa E501
                "napytau.import_export.crawler.file_crawler": file_crawler_module_mock,  # noqa E501
                "napytau.import_export.reader.file_reader": file_reader_module_mock,  # noqa E501
            },
        ):
            from napytau.import_export.import_export import ingest_napatau_format_from_files

            ingest_napatau_format_from_files("test_directory", "test.fit")
            self.assertEqual(
                file_crawler_module_mock.FileCrawler.mock_calls[0].args[0],
                ["v_c", "distances.dat", "norm.fac"],
            )

    @staticmethod
    def test_callsTheCrawlersCrawlMethodWithTheProvidedDirectoryPath():
        """Calls the crawler's crawl method with the provided directory path."""
        (
            napatau_dataset_factory_module_mock,
            file_crawler_module_mock,
            file_reader_module_mock,
        ) = set_up_mocks()
        with patch.dict(
            "sys.modules",
            {
                "napytau.import_export.dataset_factory.napatau_dataset_factory": napatau_dataset_factory_module_mock,  # noqa E501
                "napytau.import_export.crawler.file_crawler": file_crawler_module_mock,  # noqa E501
                "napytau.import_export.reader.file_reader": file_reader_module_mock,  # noqa E501
            },
        ):
            from napytau.import_export.import_export import ingest_napatau_format_from_files

            ingest_napatau_format_from_files("test_directory")
            file_crawler_module_mock.FileCrawler.mock_calls[0].crawl("test_directory")

    def test_readsEveryFileReturnedByTheFileCrawler(self):
        """Reads every file returned by the file crawler."""
        (
            napatau_dataset_factory_module_mock,
            file_crawler_module_mock,
            file_reader_module_mock,
        ) = set_up_mocks()
        file_crawler_module_mock.FileCrawler.return_value = (
            file_crawler_module_mock.FileCrawler
        )
        file_crawler_module_mock.FileCrawler.crawl.return_value = [
            NapatauSetupFiles(
                "test_distances.dat",
                "test_v_c",
                "test_fit",
                "test_norm.fac",
            )
        ]

        with patch.dict(
            "sys.modules",
            {
                "napytau.import_export.dataset_factory.napatau_dataset_factory": napatau_dataset_factory_module_mock,  # noqa E501
                "napytau.import_export.crawler.file_crawler": file_crawler_module_mock,  # noqa E501
                "napytau.import_export.reader.file_reader": file_reader_module_mock,  # noqa E501
            },
        ):
            from napytau.import_export.import_export import ingest_napatau_format_from_files

            ingest_napatau_format_from_files("test_directory")
            self.assertEqual(
                file_reader_module_mock.FileReader.read_rows.mock_calls[0].args[0],
                "test_v_c",
            )
            self.assertEqual(
                file_reader_module_mock.FileReader.read_rows.mock_calls[1].args[0],
                "test_distances.dat",
            )
            self.assertEqual(
                file_reader_module_mock.FileReader.read_rows.mock_calls[2].args[0],
                "test_fit",
            )
            self.assertEqual(
                file_reader_module_mock.FileReader.read_rows.mock_calls[3].args[0],
                "test_norm.fac",
            )

    def test_callsTheNapatauDatasetFactoryWithTheRawNapatauDataIfNoFitFileIsProvided(
        self,
    ):
        """Calls the napatau dataset factory with the raw napatau data."""
        (
            napatau_dataset_factory_module_mock,
            file_crawler_module_mock,
            file_reader_module_mock,
        ) = set_up_mocks()
        file_crawler_module_mock.FileCrawler.return_value = (
            file_crawler_module_mock.FileCrawler
        )
        file_crawler_module_mock.FileCrawler.crawl.return_value = [
            NapatauSetupFiles(
                "test_distances.dat",
                "test_v_c",
                "test_fit",
                "test_norm.fac",
            )
        ]
        file_reader_module_mock.FileReader.read_rows.side_effect = [
            ["v_c_row"],
            ["distances.dat_row"],
            ["fit_row"],
            ["calibration_row"],
        ]

        with patch.dict(
            "sys.modules",
            {
                "napytau.import_export.dataset_factory.napatau_dataset_factory": napatau_dataset_factory_module_mock,  # noqa E501
                "napytau.import_export.crawler.file_crawler": file_crawler_module_mock,  # noqa E501
                "napytau.import_export.reader.file_reader": file_reader_module_mock,  # noqa E501
            },
        ):
            from napytau.import_export.import_export import ingest_napatau_format_from_files

            ingest_napatau_format_from_files("test_directory")
            self.assertEqual(
                napatau_dataset_factory_module_mock.NapatauDatasetFactory.create_dataset.mock_calls[
                    0
                ]
                .args[0]
                .velocity_rows,
                ["v_c_row"],
            )
            self.assertEqual(
                napatau_dataset_factory_module_mock.NapatauDatasetFactory.create_dataset.mock_calls[
                    0
                ]
                .args[0]
                .distance_rows,
                ["distances.dat_row"],
            )
            self.assertEqual(
                napatau_dataset_factory_module_mock.NapatauDatasetFactory.create_dataset.mock_calls[
                    0
                ]
                .args[0]
                .fit_rows,
                ["fit_row"],
            )
            self.assertEqual(
                napatau_dataset_factory_module_mock.NapatauDatasetFactory.create_dataset.mock_calls[
                    0
                ]
                .args[0]
                .calibration_rows,
                ["calibration_row"],
            )

    def test_callsTheNapatauDatasetFactoryWithTheRawNapatauDataIfAFitFileIsProvided(
        self,
    ):
        """Calls the napatau dataset factory with the raw napatau data."""
        (
            napatau_dataset_factory_module_mock,
            file_crawler_module_mock,
            file_reader_module_mock,
        ) = set_up_mocks()
        file_crawler_module_mock.FileCrawler.return_value = (
            file_crawler_module_mock.FileCrawler
        )
        file_crawler_module_mock.FileCrawler.crawl.return_value = [
            NapatauSetupFiles(
                "test_distances.dat",
                "test_v_c",
                "test_fit",
                "test_norm.fac",
            )
        ]
        file_reader_module_mock.FileReader.read_rows.side_effect = [
            ["v_c_row"],
            ["distances.dat_row"],
            ["fit_row"],
            ["calibration_row"],
        ]

        with patch.dict(
            "sys.modules",
            {
                "napytau.import_export.dataset_factory.napatau_dataset_factory": napatau_dataset_factory_module_mock,  # noqa E501
                "napytau.import_export.crawler.file_crawler": file_crawler_module_mock,  # noqa E501
                "napytau.import_export.reader.file_reader": file_reader_module_mock,  # noqa E501
            },
        ):
            from napytau.import_export.import_export import ingest_napatau_format_from_files

            ingest_napatau_format_from_files("test_directory", "test.fit")
            self.assertEqual(
                napatau_dataset_factory_module_mock.NapatauDatasetFactory.create_dataset.mock_calls[
                    0
                ]
                .args[0]
                .velocity_rows,
                ["v_c_row"],
            )
            self.assertEqual(
                napatau_dataset_factory_module_mock.NapatauDatasetFactory.create_dataset.mock_calls[
                    0
                ]
                .args[0]
                .distance_rows,
                ["distances.dat_row"],
            )
            self.assertEqual(
                napatau_dataset_factory_module_mock.NapatauDatasetFactory.create_dataset.mock_calls[
                    0
                ]
                .args[0]
                .fit_rows,
                ["fit_row"],
            )
            self.assertEqual(
                napatau_dataset_factory_module_mock.NapatauDatasetFactory.create_dataset.mock_calls[
                    0
                ]
                .args[0]
                .calibration_rows,
                ["calibration_row"],
            )


if __name__ == "__main__":
    unittest.main()
