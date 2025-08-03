"""
Tests for the main FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test that the application is running"""
    response = client.get("/")
    assert response.status_code == 200


def test_websocket_endpoint():
    """Test WebSocket endpoint structure"""
    # This is a basic test - actual WebSocket testing would require more setup
    assert hasattr(app, 'router')
    # Check if the WebSocket route exists
    routes = [route.path for route in app.routes]
    assert any('/ws/' in route for route in routes)


def test_executions_endpoint():
    """Test executions endpoint structure"""
    # Test with a dummy wallet address
    response = client.get("/executions/test_wallet")
    # Should return 200 or appropriate error code
    assert response.status_code in [200, 404, 422]


def test_open_orders_endpoint():
    """Test open orders endpoint structure"""
    # Test with a dummy wallet address
    response = client.get("/open_orders/test_wallet")
    # Should return 200 or appropriate error code
    assert response.status_code in [200, 404, 422]


def test_cors_headers():
    """Test that CORS headers are properly set"""
    response = client.options("/")
    assert "access-control-allow-origin" in response.headers


if __name__ == "__main__":
    pytest.main([__file__]) 