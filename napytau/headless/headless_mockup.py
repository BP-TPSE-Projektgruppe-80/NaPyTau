from typing import List

from napytau.cli.cli_arguments import CLIArguments
from napytau.ingest.ingest import (
    INGEST_FORMAT_NAPATAU,
    ingest_napatau_format_from_files,
)
from napytau.ingest.model.dataset import DataSet


def init(cli_arguments: CLIArguments) -> None:
    if cli_arguments.get_dataset_format() == INGEST_FORMAT_NAPATAU:
        setup_files_directory_path = cli_arguments.get_setup_files_directory_path()
        if setup_files_directory_path is None:
            raise ValueError("No setup files directory provided")

        datasets: List[DataSet] = ingest_napatau_format_from_files(
            setup_files_directory_path,
            cli_arguments.get_fit_file_path(),
        )

        for dataset in datasets:
            print("Dataset:")
            print(f"  Velocity: {dataset.relative_velocity.velocity}")
            for datapoint in dataset.datapoints:
                print("  Datapoint:")
                print(
                    f"    Distance: Value: {datapoint.get_distance().value} "
                    f"Error: {datapoint.get_distance().error}"
                )
                print(
                    f"    Calibration: Value: {datapoint.get_calibration().value} "
                    f"Error: {datapoint.get_calibration().error}"
                )
                shifted_intensity, unshifted_intensity = datapoint.get_intensity()
                print(
                    f"    Shifted Intensity: Value: {shifted_intensity.value} "
                    f"Error: {shifted_intensity.error}"
                )
                print(
                    f"    Unshifted Intensity: Value: {unshifted_intensity.value} "
                    f"Error: {unshifted_intensity.error}"
                )
                print("-" * 80)
            print("=" * 80)

    else:
        raise ValueError(
            f"Unknown dataset format: {cli_arguments.get_dataset_format()}"
        )
