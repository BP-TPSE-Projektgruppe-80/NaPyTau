from pathlib import PurePath
from typing import List

from napytau.cli.cli_arguments import CLIArguments
from napytau.import_export.import_export import (
    IMPORT_FORMAT_NAPATAU,
    import_napatau_format_from_files,
)
from napytau.import_export.model.dataset import DataSet


def init(cli_arguments: CLIArguments) -> None:
    if cli_arguments.get_dataset_format() == IMPORT_FORMAT_NAPATAU:
        setup_files_directory_path = cli_arguments.get_setup_files_directory_path()

        fit_fie_path = cli_arguments.get_fit_file_path()

        datasets: List[DataSet] = import_napatau_format_from_files(
            PurePath(setup_files_directory_path),
            PurePath(fit_fie_path) if fit_fie_path else None,
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
