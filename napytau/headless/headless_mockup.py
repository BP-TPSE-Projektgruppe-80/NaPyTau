from pathlib import PurePath
from typing import List

from napytau.cli.cli_arguments import CLIArguments
from napytau.import_export.import_export import (
    IMPORT_FORMAT_NAPATAU,
    import_napatau_format_from_files,
    read_napatau_setup_data_into_data_set,
)
from napytau.import_export.model.dataset import DataSet
from napytau.util.coalesce import coalesce


def init(cli_arguments: CLIArguments) -> None:
    if cli_arguments.get_dataset_format() == IMPORT_FORMAT_NAPATAU:
        setup_files_directory_path = cli_arguments.get_data_files_directory_path()

        fit_file_path = cli_arguments.get_fit_file_path()

        datasets: List[DataSet] = import_napatau_format_from_files(
            PurePath(setup_files_directory_path),
            PurePath(fit_file_path) if fit_file_path else None,
        )

        for dataset in datasets:
            print("Dataset:")
            print(f"  Velocity: {dataset.relative_velocity.value.get_velocity()}")
            print(f"  Velocity Error: {dataset.relative_velocity.error.get_velocity()}")
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
                print(f"    Active:  {datapoint.is_active()} ")
                print("-" * 80)
            print("=" * 80)

        setup_file_path = cli_arguments.get_setup_file_path()
        if setup_file_path is not None:
            for dataset in datasets:
                read_napatau_setup_data_into_data_set(
                    dataset, PurePath(setup_file_path)
                )

                print("Dataset:")
                print(f"  Velocity: {dataset.relative_velocity.value.get_velocity()}")
                print(
                    f"  Velocity Error: {dataset.relative_velocity.error.get_velocity()}"  # noqa: E501
                )
                print(f"  Tau factor: {dataset.get_tau_factor()}")
                print(f"  Polynomial count: {dataset.get_polynomial_count()}")

                for index, sampling_point in enumerate(
                    coalesce(dataset.get_sampling_points(), [])
                ):
                    print(f"  Sampling point #{index}: {sampling_point}")

                for datapoint in dataset.datapoints:
                    print("  Datapoint:")
                    print(
                        f"    Distance: Value: {datapoint.get_distance().value} "
                        f"Error: {datapoint.get_distance().error}"
                    )
                    print(f"    Active:  {datapoint.is_active()} ")
                    print("-" * 80)
                print("=" * 80)

    else:
        raise ValueError(
            f"Unknown dataset format: {cli_arguments.get_dataset_format()}"
        )
