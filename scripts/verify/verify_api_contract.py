import asyncio
from httpx import AsyncClient, ASGITransport
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
from app.main import app

async def verify_contracts():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Test 1: Successful response structure
        # (Assuming /api/v1/health returns success)
        response = await client.get("/api/v1/health")
        data = response.json()
        
        assert "success" in data, "Missing 'success' in response envelope"
        assert data["success"] is True, "Success should be True"
        assert "data" in data, "Missing 'data' in response envelope"
        assert "meta" in data, "Missing 'meta' in response envelope"
        
        # Test 2: Error response structure
        # (Assuming a POST to health without body or to missing endpoint)
        response = await client.post("/api/v1/organizations/", json={})
        data = response.json()
        
        assert "success" in data, "Missing 'success' in error envelope"
        assert data["success"] is False, "Success should be False for error"
        assert "error" in data, "Missing 'error' in error envelope"
        assert "code" in data["error"], "Missing 'code' in error object"
        assert "message" in data["error"], "Missing 'message' in error object"
        assert "request_id" in data["error"], "Missing 'request_id' in error object"

if __name__ == "__main__":
    print("Running API Contract Validation...")
    asyncio.run(verify_contracts())
    print("✅ API Contract Validation Passed. Envelope structures verified.")
