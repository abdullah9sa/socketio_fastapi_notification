## this file tests the socket using pytest, when running this file using "pytest pytst.py", it sends a notification and assert the recived notification with the sent.

import pytest
import websockets
from fastapi.testclient import TestClient
from app.main import app  # Replace with the actual import path of your FastAPI app

# Mock the WebSocket communication using monkeypatch
# this is used to simulate the interaction with a WebSocket connection without making real network calls
class MockWebSocket:
    async def send(self, message):
        self.message = message

    async def receive(self):
        return self.message

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_websocket(client, monkeypatch):
    # Create a mock WebSocket
    mock_websocket = MockWebSocket()

    # Monkeypatch the websocket connect function to use the mock WebSocket
    monkeypatch.setattr(websockets, "connect", lambda uri: mock_websocket)

    # Send a notification using the send_notification route
    notification = "Test message"
    response = client.post(f"/send_notification?notification={notification}")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Simulate receiving the notification through the mock WebSocket
    mock_websocket.message = notification
    # Receive the response from the WebSocket
    websocket_response = await mock_websocket.receive()

    # Assert that the received message matches the sent notification
    assert websocket_response == notification
