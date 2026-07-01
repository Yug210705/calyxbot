"""Tests for the Calyx API root application.

Verifies the application factory creates a working FastAPI instance
and the root endpoint returns the expected service identification.
"""

from fastapi import status
from fastapi.testclient import TestClient

from app.main import APP_VERSION, app

client = TestClient(app)


class TestRootEndpoint:
    """Verify the root endpoint returns service identification."""

    def test_returns_200_ok(self) -> None:
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK

    def test_returns_correct_service_name(self) -> None:
        response = client.get("/")
        assert response.json()["service"] == "calyx-api"

    def test_returns_ok_status(self) -> None:
        response = client.get("/")
        assert response.json()["status"] == "ok"

    def test_returns_current_version(self) -> None:
        response = client.get("/")
        assert response.json()["version"] == APP_VERSION

    def test_response_contains_only_expected_fields(self) -> None:
        response = client.get("/")
        assert set(response.json().keys()) == {"status", "service", "version"}

    def test_response_content_type_is_json(self) -> None:
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"


class TestOpenAPIDocumentation:
    """Verify API documentation endpoints are accessible."""

    def test_swagger_ui_is_accessible(self) -> None:
        response = client.get("/docs")
        assert response.status_code == status.HTTP_200_OK

    def test_redoc_is_accessible(self) -> None:
        response = client.get("/redoc")
        assert response.status_code == status.HTTP_200_OK

    def test_openapi_schema_is_accessible(self) -> None:
        response = client.get("/openapi.json")
        assert response.status_code == status.HTTP_200_OK

    def test_openapi_schema_has_correct_title(self) -> None:
        response = client.get("/openapi.json")
        assert response.json()["info"]["title"] == "Calyx API"

    def test_openapi_schema_has_correct_version(self) -> None:
        response = client.get("/openapi.json")
        assert response.json()["info"]["version"] == APP_VERSION
