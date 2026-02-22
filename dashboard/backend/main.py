import traceback
import json
from fastapi import FastAPI, WebSocket
from src.state.cmd_queue import cmd_queue
from src.utils.format_msg import format_message
from pathlib import Path
import asyncio
import subprocess
# from api.v1.api_v1 import api_router
from src.state.con_manager import ConnectionManager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.core_serial import core_serial_task
import logging

app = FastAPI()
logger = logging.getLogger(__name__)
# app.include_router(api_router)

socket_manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(core_serial_task(socket_manager))
    
    async def delayed_refresh():
        await asyncio.sleep(5)
        try:
            subprocess.run(["xdotool", "search", "--class", "chromium", "key", "F5"], env={"DISPLAY": ":0"})
            print("Kiosk refresh signal sent!")
        except Exception as e:
            print(f"Refresh failed (normal if browser not open yet): {e}")

    asyncio.create_task(delayed_refresh())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await socket_manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        print(f"Received data: {data}")
        await cmd_queue.put(data)
        payload = format_message(data)
        await websocket.send_text(json.dumps(payload))
        await asyncio.sleep(0)

FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="static")
else:
    print(f"Warning: Frontend path {FRONTEND_DIST} not found!")
"""
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="static")"""
