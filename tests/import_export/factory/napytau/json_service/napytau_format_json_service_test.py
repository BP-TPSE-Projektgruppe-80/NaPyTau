import unittest
from unittest.mock import MagicMock, patch

from napytau.import_export.import_export_error import ImportExportError
from napytau.import_export.model.datapoint_collection import DatapointCollection
from napytau.import_export.model.dataset import DataSet
from napytau.import_export.model.relative_velocity import RelativeVelocity
from napytau.util.model.value_error_pair import ValueErrorPair


def set_up_mocks() -> (MagicMock, MagicMock):
    json_module_mock = MagicMock()
    json_module_mock.loads = MagicMock()
    json_module_mock.JSONDecodeError = BaseException
    jsonschema_module_mock = MagicMock()
    jsonschema_module_mock.validate = MagicMock()
    jsonschema_module_mock.ValidationError = BaseException

    return json_module_mock, jsonschema_module_mock


class NapytauFormatJsonServiceUnitTest(unittest.TestCase):
    def test_raisesAnImportExportErrorWhenTheRawDataCanNotBeParsed(self):
        """Raises an ImportExportError when the raw data can not be parsed."""
        json_module_mock, jsonschema_module_mock = set_up_mocks()
        json_module_mock.loads.side_effect = BaseException("error")

        with patch.dict(
                "sys.modules",
                {
                    "json": json_module_mock,
                    "jsonschema": jsonschema_module_mock,
                },
        ):
            from napytau.import_export.factory.napytau.json_service.napytau_format_json_service import (
                NapytauFormatJsonService,
            )  # noqa E501

            with self.assertRaises(ImportExportError):
                NapytauFormatJsonService.parse_json_data("")

    def test_usesTheJsonModuleToLoadTheRawData(self):
        """Uses the json module to load the raw data."""
        json_module_mock, jsonschema_module_mock = set_up_mocks()

        json_module_mock.loads.return_value = {}

        with patch.dict(
                "sys.modules",
                {
                    "json": json_module_mock,
                    "jsonschema": jsonschema_module_mock,
                },
        ):
            from napytau.import_export.factory.napytau.json_service.napytau_format_json_service import (
                NapytauFormatJsonService,
            )  # noqa E501

            data = NapytauFormatJsonService.parse_json_data("{}")
            json_module_mock.loads.assert_called_once_with("{}")

            self.assertEqual(data, {})

    def test_usesTheJsonModuleToLoadTheSchema(self):
        """Uses the json module to load the schema."""
        json_module_mock, jsonschema_module_mock = set_up_mocks()

        json_module_mock.loads.return_value = {}

        with patch.dict(
                "sys.modules",
                {
                    "json": json_module_mock,
                    "jsonschema": jsonschema_module_mock,
                },
        ):
            from napytau.import_export.factory.napytau.json_service.napytau_format_json_service import (
                NapytauFormatJsonService,
                _SCHEMA,
            )  # noqa E501

            NapytauFormatJsonService.validate_against_schema({})
            json_module_mock.loads.assert_called_once_with(_SCHEMA)

    def test_raisesAnImportExportErrorWhenTheRawDataDoesNotMatchTheSchema(self):
        """Raises an ImportExportError when the raw data does not match the schema."""
        json_module_mock, jsonschema_module_mock = set_up_mocks()
        jsonschema_module_mock.validate.side_effect = BaseException("error")

        with patch.dict(
                "sys.modules",
                {
                    "json": json_module_mock,
                    "jsonschema": jsonschema_module_mock,
                },
        ):
            from napytau.import_export.factory.napytau.json_service.napytau_format_json_service import (
                NapytauFormatJsonService,
            )  # noqa E501

            with self.assertRaises(ImportExportError):
                NapytauFormatJsonService.validate_against_schema({})

    def test_usesTheJsonSchemaModuleToValidateTheRawData(self):
        """Uses the json schema module to validate the raw data."""
        json_module_mock, jsonschema_module_mock = set_up_mocks()

        json_module_mock.loads.return_value = {}
        jsonschema_module_mock.validate.return_value = None

        with patch.dict(
                "sys.modules",
                {
                    "json": json_module_mock,
                    "jsonschema": jsonschema_module_mock,
                },
        ):
            from napytau.import_export.factory.napytau.json_service.napytau_format_json_service import (
                NapytauFormatJsonService,
            )  # noqa E501

            self.assertTrue(NapytauFormatJsonService.validate_against_schema({}))
            jsonschema_module_mock.validate.assert_called_once_with(
                instance={},
                schema={},
            )

    def test_raisesAnImportExportErrorWhenTheProvidedDatasetCanNotBeConvertedToJSON(
        self,
    ):
        """Raises an ImportExportError when the provided dataset can not be converted to JSON."""
        json_module_mock, jsonschema_module_mock = set_up_mocks()
        json_module_mock.dumps.side_effect = ValueError("error")

        with patch.dict(
            "sys.modules",
            {
                "json": json_module_mock,
                "jsonschema": jsonschema_module_mock,
            },
        ):
            from napytau.import_export.factory.napytau.json_service.napytau_format_json_service import (
                NapytauFormatJsonService,
            )

            dataset = DataSet(
                ValueErrorPair(RelativeVelocity(1), RelativeVelocity(0.1)),
                DatapointCollection([]),
            )

            with self.assertRaises(ImportExportError):
                NapytauFormatJsonService.create_calculation_data_json_string(dataset)

    def test_usesTheJsonModuleToDumpTheProvidedDataset(self):
        """Uses the json module to dump the provided dataset."""
        json_module_mock, jsonschema_module_mock = set_up_mocks()
        json_module_mock.dumps.return_value = ""

        with patch.dict(
            "sys.modules",
            {
                "json": json_module_mock,
                "jsonschema": jsonschema_module_mock,
            },
        ):
            from napytau.import_export.factory.napytau.json_service.napytau_format_json_service import (
                NapytauFormatJsonService,
            )

            dataset = DataSet(
                relative_velocity=ValueErrorPair(
                    RelativeVelocity(1), RelativeVelocity(0.1)
                ),
                datapoints=DatapointCollection([]),
                tau_factor=1.0,
                weighted_mean_tau=ValueErrorPair(2.0, 1.1),
                sampling_points=[],
                polynomial_count=2,
                polynomials=[],
            )

            NapytauFormatJsonService.create_calculation_data_json_string(dataset)
            print(json_module_mock.dumps.call_args_list)
            json_module_mock.dumps.assert_called_once_with(
                obj={
                    "tauFactor": 1.0,
                    "weightedMeanTau": 2.0,
                    "weightedMeanTauError": 1.1,
                    "datapoints": [],
                    "samplingPoints": [],
                    "polynomials": [],
                },
                indent=2,
            )


if __name__ == "__main__":
    unittest.main()
