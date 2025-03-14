from napytau.import_export.model.dataset import DataSet
from napytau.util.coalesce import coalesce


def log_dataset(dataset: DataSet) -> None:
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


def log_dataset_setup_data(dataset: DataSet) -> None:
    print("Dataset:")
    print(f"  Velocity: {dataset.relative_velocity.value.get_velocity()}")
    print(
        f"  Velocity Error: {dataset.relative_velocity.error.get_velocity()}"
        # noqa: E501
    )
    print(f"  Tau factor: {dataset.get_tau_factor()}")
    print(f"  Polynomial count: {dataset.get_polynomial_count()}")

    for index, sampling_point in enumerate(coalesce(dataset.get_sampling_points(), [])):
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
