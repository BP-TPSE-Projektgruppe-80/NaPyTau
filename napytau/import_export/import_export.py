from typing import Optional, List

from napytau.import_export.dataset_factory.napatau_dataset_factory import (
    NapatauDatasetFactory,
)
from napytau.import_export.dataset_factory.raw_napatau_data import RawNapatauData
from napytau.import_export.crawler.file_crawler import FileCrawler
from napytau.import_export.crawler.napatau_setup_files import NapatauSetupFiles
from napytau.import_export.model.dataset import DataSet
from napytau.import_export.reader.file_reader import FileReader


def ingest_napatau_format_from_files(
    directory_path: str, fit_file_path: Optional[str] = None
) -> List[DataSet]:
    """
    Ingests a dataset from the Napatau format. The directory path will be
    recursively searched for the following files:
    - v_c
    - distances.dat
    - norm.fac
    - optional: *.fit

    if the fit_file_path is provided, the fit file will be
    read from this path instead of the directory.
    """

    file_crawler = _configure_file_crawler(fit_file_path)

    setup_file_bundles: List[NapatauSetupFiles] = file_crawler.crawl(directory_path)

    return list(
        map(
            lambda setup_files: NapatauDatasetFactory.create_dataset(
                RawNapatauData(
                    FileReader.read_rows(setup_files.velocity_file),
                    FileReader.read_rows(setup_files.distances_file),
                    FileReader.read_rows(setup_files.fit_file),
                    FileReader.read_rows(setup_files.calibration_file),
                )
            ),
            setup_file_bundles,
        )
    )


def _configure_file_crawler(fit_file_path: Optional[str]) -> FileCrawler:
    if fit_file_path:
        file_crawler = FileCrawler(
            ["v_c", "distances.dat", "norm.fac"],
            lambda files: NapatauSetupFiles.create_from_file_names(
                files + [fit_file_path]
            ),
        )

    else:
        file_crawler = FileCrawler(
            ["v_c", "distances.dat", "norm.fac", ".*.fit"],
            lambda files: NapatauSetupFiles.create_from_file_names(files),
        )
    return file_crawler
