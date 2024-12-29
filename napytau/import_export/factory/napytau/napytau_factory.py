from typing import List

from napytau.import_export.factory.napytau.json_service.napytau_format_json_service import (
    NapytauFormatJsonService,
)
from napytau.import_export.model.datapoint import Datapoint
from napytau.import_export.model.datapoint_collection import DatapointCollection
from napytau.import_export.model.dataset import DataSet
from napytau.util.model.value_error_pair import ValueErrorPair


class NapyTauFactory:
    @staticmethod
    def create_dataset(raw_json_data: dict) -> DataSet:
        NapytauFormatJsonService.validate_against_schema(raw_json_data)

        return DataSet(
            ValueErrorPair(
                raw_json_data["relativeVelocity"],
                raw_json_data["relativeVelocityError"],
            ),
            NapyTauFactory.parse_datapoints(raw_json_data["datapoints"]),
        )

    @staticmethod
    def parse_datapoints(raw_datapoints: List[dict]) -> DatapointCollection:
        datapoints = []
        for raw_datapoint in raw_datapoints:
            distance = ValueErrorPair(
                raw_datapoint.get("distance"),
                raw_datapoint.get("distanceError"),
            )
            calibration = ValueErrorPair(
                raw_datapoint.get("calibration"),
                raw_datapoint.get("calibrationError"),
            )
            shifted_intensity = ValueErrorPair(
                raw_datapoint.get("shiftedIntensity"),
                raw_datapoint.get("shiftedIntensityError"),
            )
            unshifted_intensity = ValueErrorPair(
                raw_datapoint.get("unshiftedIntensity"),
                raw_datapoint.get("unshiftedIntensityError"),
            )

            if "feedingShiftedIntensity" in raw_datapoint:
                feeding_shifted_intensity = ValueErrorPair(
                    raw_datapoint["feedingShiftedIntensity"],
                    raw_datapoint["feedingShiftedIntensityError"],
                )
                feeding_unshifted_intensity = ValueErrorPair(
                    raw_datapoint["feedingUnshiftedIntensity"],
                    raw_datapoint["feedingUnshiftedIntensityError"],
                )
            else:
                feeding_shifted_intensity = None
                feeding_unshifted_intensity = None

            datapoints.append(
                Datapoint(
                    distance,
                    calibration,
                    shifted_intensity,
                    unshifted_intensity,
                    feeding_shifted_intensity,
                    feeding_unshifted_intensity,
                )
            )

        return DatapointCollection(datapoints)
