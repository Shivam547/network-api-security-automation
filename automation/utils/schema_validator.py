import json
from pathlib import Path

from jsonschema import validate


def validate_response_schema(response, schema_file):
    """
    Validate an API response against a JSON schema.
    """

    schema_path = Path(schema_file)

    with open(schema_path, "r") as file:
        schema = json.load(file)

    validate(
        instance=response.json(),
        schema=schema
    )