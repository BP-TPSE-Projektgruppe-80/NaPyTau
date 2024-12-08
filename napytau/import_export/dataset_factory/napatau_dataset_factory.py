from typing import List, Optional, Tuple

from napytau.import_export.dataset_factory.raw_napatau_data import RawNapatauData
from napytau.import_export.model.datapoint import Datapoint
from napytau.import_export.model.datapoint_collection import DatapointCollection
from napytau.import_export.model.dataset import DataSet
from napytau.import_export.model.relative_velocity import RelativeVelocity
from napytau.util.model.value_error_pair import ValueErrorPair


class NapatauDatasetFactory:
    @staticmethod
    def create_dataset(raw_dataset: RawNapatauData) -> DataSet:
        return DataSet(
            NapatauDatasetFactory.parse_velocity(raw_dataset.velocity_rows),
            NapatauDatasetFactory.parse_datapoints(
                raw_dataset.distance_rows,
                raw_dataset.calibration_rows,
                raw_dataset.fit_rows,
            ),
        )

    @staticmethod
    def parse_velocity(velocity_rows: List[str]) -> RelativeVelocity:
        filtered_velocities = list(
            filter(lambda x: not x.startswith("#"), velocity_rows)
        )

        if len(filtered_velocities) != 1:
            raise ValueError(
                f"Expected one velocity row, but got {len(filtered_velocities)}"
            )

        return RelativeVelocity(float(filtered_velocities[0]))

    @staticmethod
    def parse_datapoints(
        distance_rows: List[str],
        calibration_rows: List[str],
        fit_rows: List[str],
    ) -> DatapointCollection:
        datapoints = DatapointCollection([])
        for distance_row in distance_rows:
            distance = NapatauDatasetFactory.parse_distance_row(distance_row)
            datapoints.add_datapoint(Datapoint(distance))
        for calibration_row in calibration_rows:
            (distance_index, calibration) = NapatauDatasetFactory.parse_calibration_row(
                calibration_row
            )
            datapoint = datapoints.get_datapoint_by_distance(distance_index)
            datapoint.set_calibration(calibration)
        for fit_row in fit_rows:
            (
                distance_index,
                shifted_intensity,
                unshifted_intensity,
                feeding_shifted_intensity,
                feeding_unshifted_intensity,
            ) = NapatauDatasetFactory.parse_fit_row(fit_row)
            datapoint = datapoints.get_datapoint_by_distance(distance_index)
            datapoint.set_intensity(shifted_intensity, unshifted_intensity)
            if (
                feeding_shifted_intensity is not None
                and feeding_unshifted_intensity is not None
            ):
                datapoint.set_feeding_intensity(
                    feeding_shifted_intensity, feeding_unshifted_intensity
                )

        return datapoints

    @staticmethod
    def parse_distance_row(distance_row: str) -> ValueErrorPair[float]:
        split_row = distance_row.split(" ")
        if len(split_row) < 3:
            raise ValueError(
                f"Expected at least 3 values in distance row, but got {len(split_row)}"
            )

        if len(split_row) > 3:
            raise ValueError(
                f"Expected at most 3 values in distance row, but got {len(split_row)}"
            )

        # The first value (at index 0) is a label, however since we index by distance we can ignore it # noqa E501
        distance = float(split_row[1])
        distance_error = float(split_row[2])

        return ValueErrorPair(distance, distance_error)

    @staticmethod
    def parse_calibration_row(
        calibration_row: str,
    ) -> Tuple[float, ValueErrorPair[float]]:
        split_row = calibration_row.split(" ")
        if len(split_row) < 3:
            raise ValueError(
                f"Expected at least 3 values in calibration row, but got {len(split_row)}"  # noqa E501
            )

        if len(split_row) > 3:
            raise ValueError(
                f"Expected at most 3 values in calibration row, but got {len(split_row)}"  # noqa E501
            )

        distance_index = float(split_row[0])
        calibration = float(split_row[1])
        calibration_error = float(split_row[2])

        return distance_index, ValueErrorPair(calibration, calibration_error)

    @staticmethod
    def parse_fit_row(
        fit_row: str,
    ) -> Tuple[
        float,
        ValueErrorPair[float],
        ValueErrorPair[float],
        Optional[ValueErrorPair[float]],
        Optional[ValueErrorPair[float]],
    ]:
        split_row = fit_row.split(" ")
        if len(split_row) < 5:
            raise ValueError(
                f"Expected at least 5 values in fit row, but got {len(split_row)}"
            )

        distance_index = float(split_row[0])
        shifted_intensity = float(split_row[1])
        shifted_intensity_error = float(split_row[2])
        unshifted_intensity = float(split_row[3])
        unshifted_intensity_error = float(split_row[4])

        if len(split_row) == 5:
            return (
                distance_index,
                ValueErrorPair(shifted_intensity, shifted_intensity_error),
                ValueErrorPair(unshifted_intensity, unshifted_intensity_error),
                None,
                None,
            )

        if len(split_row) < 9:
            raise ValueError(
                f"Expected at least 9 values in fit row, but got {len(split_row)}"
            )

        if len(split_row) > 9:
            raise ValueError(
                f"Expected at most 9 values in fit row, but got {len(split_row)}"
            )

        feeding_shifted_intensity = float(split_row[5])
        feeding_shifted_intensity_error = float(split_row[6])
        feeding_unshifted_intensity = float(split_row[7])
        feeding_unshifted_intensity_error = float(split_row[8])

        return (
            distance_index,
            ValueErrorPair(shifted_intensity, shifted_intensity_error),
            ValueErrorPair(unshifted_intensity, unshifted_intensity_error),
            ValueErrorPair(feeding_shifted_intensity, feeding_shifted_intensity_error),
            ValueErrorPair(
                feeding_unshifted_intensity, feeding_unshifted_intensity_error
            ),
        )
