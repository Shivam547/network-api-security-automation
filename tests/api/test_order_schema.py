from pathlib import Path

from automation.utils.schema_validator import validate_response_schema


SCHEMA_PATH = (
    Path(__file__).parent.parent.parent
    / "automation"
    / "schemas"
    / "order_response.json"
)


def test_get_order_response_schema(admin_client):

    response = admin_client.get("/orders/1")

    assert response.status_code == 200

    validate_response_schema(
        response,
        SCHEMA_PATH
    )