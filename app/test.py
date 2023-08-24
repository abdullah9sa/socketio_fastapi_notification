## this file tests the socket using websockets, when running this file, it listens to every notification sent to the server.
## this file runs seperatly from the fastapi server.

import asyncio
import websockets

async def listen_to_socket():
    uri = "ws://localhost:8000/ws"  # since the fastapi sevser is hosted locally, ws is the socket route
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                print(f"Received notification: {message}")
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed.")
                break

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(listen_to_socket())
