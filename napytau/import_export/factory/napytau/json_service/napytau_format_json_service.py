import json
import jsonschema

from napytau.import_export.import_export_error import ImportExportError


class NapytauFormatJsonService:
    @staticmethod
    def parse_json_data(json_string: str) -> dict:
        """
        Parses the provided json data into a dictionary
        """

        try:
            json_data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ImportExportError(f"Provided json data could not be parsed: {e}")

        return json_data

    @staticmethod
    def validate_against_schema(json_data: dict) -> bool:
        """
        Validates the provided json data against the napytau json schema
        """

        with open("napytau.schema.json", "r") as schema_file:
            schema = json.load(schema_file)

        try:
            jsonschema.validate(instance=json_data, schema=schema)
        except jsonschema.ValidationError as e:
            raise ImportExportError(
                f"Provided json data does not match the napytau json schema: {e}"
            )

        return True
