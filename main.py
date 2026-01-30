from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

app = FastAPI()


@app.get("/")
async def index():
    return HTMLResponse(open("index.html", encoding="utf-8").read())


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    counter = 1

    try:
        while True:
            data = await ws.receive_text()
            payload = json.loads(data)

            text = payload.get("text", "")

            response = {
                "number": counter,
                "text": text
            }

            counter += 1

            await ws.send_text(json.dumps(response))

    except WebSocketDisconnect:
        pass
