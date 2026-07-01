from fastapi.testclient import TestClient

from app.core.exceptions import CalyxException
from app.main import app
from app.shared.response import create_success_response


# Add a couple of test endpoints to the app for observability testing
@app.get("/test/success")
def dummy_success_endpoint():
    return create_success_response(data={"message": "ok"}).model_dump()

@app.get("/test/calyx-error")
def dummy_calyx_error_endpoint():
    raise CalyxException(
        status_code=400,
        error_code="TEST_ERROR",
        message="A test exception occurred",
        details={"field": "value"}
    )

@app.get("/test/unhandled-error")
def dummy_unhandled_error_endpoint():
    raise ValueError("Something unexpected broke")

client = TestClient(app, raise_server_exceptions=False)

def test_request_id_generation_and_propagation():
    """Test that a Request ID is generated and returned in headers."""
    response = client.get("/test/success")
    assert response.status_code == 200

    # Header should be present
    request_id = response.headers.get("X-Request-ID")
    assert request_id is not None
    assert isinstance(request_id, str)
    assert len(request_id) > 10

def test_client_request_id_is_respected():
    """Test that a client-provided Request ID is preserved."""
    client_req_id = "test-client-id-1234"
    response = client.get("/test/success", headers={"X-Request-ID": client_req_id})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == client_req_id

def test_success_response_schema():
    """Test the unified success response format."""
    response = client.get("/test/success")
    data = response.json()

    assert data["success"] is True
    assert data["data"] == {"message": "ok"}
    assert "meta" in data
    assert "timestamp" in data["meta"]

def test_calyx_exception_response_format():
    """Test the unified error response format for CalyxExceptions."""
    response = client.get("/test/calyx-error")
    assert response.status_code == 400

    data = response.json()
    assert data["success"] is False
    assert "error" in data

    error_detail = data["error"]
    assert error_detail["code"] == "TEST_ERROR"
    assert error_detail["message"] == "A test exception occurred"
    assert error_detail["details"] == {"field": "value"}
    assert "request_id" in error_detail
    assert "timestamp" in error_detail

def test_unhandled_exception_response_format():
    """Test the unified error response format for unhandled exceptions."""
    response = client.get("/test/unhandled-error")
    assert response.status_code == 500

    data = response.json()
    assert data["success"] is False
    assert "error" in data

    error_detail = data["error"]
    assert error_detail["code"] == "INTERNAL_SERVER_ERROR"
    assert error_detail["message"] == "An unexpected error occurred."
    assert "request_id" in error_detail
    # Details shouldn't be exposed for unhandled errors
    assert "details" not in error_detail
