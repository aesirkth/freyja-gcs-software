import traceback
import json
from fastapi import FastAPI, WebSocket
from src.state.cmd_queue import cmd_queue
from pathlib import Path
import asyncio
import subprocess
# from api.v1.api_v1 import api_router
from src.state.con_manager import ConnectionManager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.core_serial import core_serial_task

app = FastAPI()
# app.include_router(api_router)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    await asyncio.sleep(3) 
    try:
        asyncio.create_task(core_serial_task(manager))
        # subprocess.run(["xdotool", "key", "F5"], env={"DISPLAY": ":0"})
        print("Kiosk refresh signal sent!")
    except Exception as e:
        print(f"Failed to refresh kiosk: {e}")
        traceback.print_exc()
        raise e

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        print(f"Received data: {data}")
        if data:
            await cmd_queue.put(data)
        payload = {
            "data": data,
        }
        await websocket.send_text(json.dumps(payload))
        await asyncio.sleep(0.1)

FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="static")
