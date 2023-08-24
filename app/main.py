### task 3 : Abdullah Salih
'''
the project consists of 3 main files.
main.py, the fastapi server with the socket initlization and send notificaiton route.
test.py tests the fastapi server socket , it listens to every notification sent to the server and prints it.
pytst.py  it sends a notification and assert the recived notification with the sent.
'''


from fastapi import FastAPI, WebSocket

app = FastAPI()

# Store a list of active WebSocket connections in an in-memory variable
active_connections = []

# the WebSocket endpoint ws
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # here should be procesing the data if needed
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)

#  route to send notifications to connected clients and return the sent notification
#  notification is sent as query parameter for simplicty although its better to send using a post request body data.
@app.post("/send_notification")
async def send_notification(notification: str):
    for connection in active_connections:
        try:
            await connection.send_text(notification)
        except Exception as e:
            print(f"Error sending notification: {e}")
    return {"notification_sent": notification}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
